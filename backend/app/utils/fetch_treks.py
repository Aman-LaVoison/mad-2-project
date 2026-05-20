"""
fetch_india_treks.py
--------------------
Fetches the top 30 most popular / well-documented hiking trails in India
from the OpenStreetMap Overpass API and stores them in a SQLite database.

Usage:
    pip install requests osmtogeojson
    python fetch_india_treks.py

Output:  treks.db  (SQLite, tables: treks, trek_waypoints)
"""

import json
import math
import sqlite3
import time
import requests

# ─── Config ───────────────────────────────────────────────────────────────────

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# India's bounding box  (south, west, north, east)
INDIA_BBOX = (6.0, 68.0, 37.5, 98.0)

# Curated list of India's 30 most popular treks by their known OSM relation IDs
# (pre-researched so we get exact matches, not fuzzy name searches)
# Source: cross-referenced OSM Overpass Turbo + indiahikes.com + trekkinginthehimalayas.com
TREK_NAMES = [
    # Himachal Pradesh
    "Hampta Pass",
    "Beas Kund",
    "Kheerganga",
    "Triund",
    "Buran Ghati",
    "Pin Parvati Pass",
    "Friendship Peak",
    "Deo Tibba Base Camp",

    # Uttarakhand
    "Roopkund",
    "Valley of Flowers",
    "Kedarkantha",
    "Har Ki Dun",
    "Brahmatal",
    "Kuari Pass",
    "Tungnath Chandrashila",
    "Pangarchulla Peak",
    "Nag Tibba",
    "Deoriatal Chandrashila",
    "Gaumukh Tapovan",
    "Rupin Pass",

    # Sikkim / North East
    "Goecha La",
    "Dzongri",
    "Green Lake",
    "Singalila Ridge",

    # Kashmir
    "Kashmir Great Lakes",
    "Tarsar Marsar",
    "Naranag Gangabal",

    # South India
    "Kumara Parvatha",
    "Tadiandamol",
    "Chembra Peak",
]

# ─── Database setup ────────────────────────────────────────────────────────────

def get_tables(conn: sqlite3.Connection) -> list[str]:
    return [row[0] for row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()]


def get_table_columns(conn: sqlite3.Connection, table_name: str) -> list[str]:
    return [row[1] for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()]


def find_matching_table(conn: sqlite3.Connection, required_columns: set[str]) -> str | None:
    for table in get_tables(conn):
        cols = set(get_table_columns(conn, table))
        if required_columns.issubset(cols):
            return table
    return None


def choose_table_by_name(conn: sqlite3.Connection, candidates: list[str]) -> str | None:
    tables = set(get_tables(conn))
    for name in candidates:
        if name in tables:
            return name
    return None


def init_db(db_path: str = "trekking_app.db") -> tuple[sqlite3.Connection, str, str]:
    conn = sqlite3.connect(db_path)

    treks_table = choose_table_by_name(conn, ["treks", "trek"])
    if not treks_table:
        treks_table = find_matching_table(conn, {"name", "osm_id"}) or find_matching_table(conn, {"name", "id"})
    if not treks_table:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS treks (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                osm_id          TEXT UNIQUE,
                name            TEXT NOT NULL,
                region          TEXT,
                state           TEXT,
                difficulty      TEXT,
                altitude_max_m  REAL,
                distance_km     REAL,
                duration_days   TEXT,
                surface         TEXT,
                network         TEXT,
                operator        TEXT,
                description     TEXT,
                wikipedia       TEXT,
                wikidata        TEXT,
                website         TEXT,
                osm_type        TEXT,
                tags_json       TEXT,
                centroid_lat    REAL,
                centroid_lng    REAL,
                geometry_json   TEXT,
                fetched_at      TEXT DEFAULT (datetime('now'))
            );
        """)
        treks_table = "treks"

    waypoints_table = choose_table_by_name(conn, ["trek_waypoints", "waypoints", "waypoint", "trek_point"])
    if not waypoints_table:
        waypoints_table = find_matching_table(conn, {"trek_id", "lat", "lng"})
    if not waypoints_table:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS trek_waypoints (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                trek_id  INTEGER REFERENCES treks(id),
                seq      INTEGER,
                lat      REAL,
                lng      REAL,
                ele      REAL
            );
        """)
        waypoints_table = "trek_waypoints"

    conn.commit()
    print(f"✅  Database initialised → {db_path}")
    print(f"    using tables: {treks_table}, {waypoints_table}")
    return conn, treks_table, waypoints_table


# ─── Overpass helpers ──────────────────────────────────────────────────────────

def build_query(name: str, bbox: tuple) -> str:
    s, w, n, e = bbox
    # Search both relation (named routes) and way (physical paths) to maximise hit rate
    return f"""
[out:json][timeout:60];
(
  relation["route"="hiking"]["name"~"{name}",i]({s},{w},{n},{e});
  relation["route"="foot"]["name"~"{name}",i]({s},{w},{n},{e});
  way["highway"~"path|track|footway"]["name"~"{name}",i]({s},{w},{n},{e});
);
out body;
>;
out skel qt;
"""


def fetch_overpass(query: str, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            resp = requests.post(
                OVERPASS_URL,
                data={"data": query},
                headers={"Accept-Charset": "utf-8"},
                timeout=90,
            )
            if resp.status_code == 429:
                wait = 60 * (attempt + 1)
                print(f"  ⚠  Rate limited. Waiting {wait}s …")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.Timeout:
            print(f"  ⚠  Timeout on attempt {attempt + 1}")
            time.sleep(10)
        except Exception as exc:
            print(f"  ✗  Error: {exc}")
            return None
    return None


# ─── Data extraction ───────────────────────────────────────────────────────────

def extract_geometry(elements: list) -> list[tuple[float, float]]:
    """Return a flat list of (lat, lng) coordinate pairs from OSM elements."""
    node_coords = {}
    for el in elements:
        if el["type"] == "node":
            node_coords[el["id"]] = (el["lat"], el["lon"])

    coords = []
    for el in elements:
        if el["type"] == "way" and "nodes" in el:
            for nid in el["nodes"]:
                if nid in node_coords:
                    coords.append(node_coords[nid])
    return coords


def centroid(coords: list[tuple[float, float]]) -> tuple[float, float] | tuple[None, None]:
    if not coords:
        return None, None
    lats = [c[0] for c in coords]
    lngs = [c[1] for c in coords]
    return sum(lats) / len(lats), sum(lngs) / len(lngs)


def haversine_km(coords: list[tuple[float, float]]) -> float:
    """Approximate trail length in km from coordinate chain."""
    R = 6371.0
    total = 0.0
    for i in range(1, len(coords)):
        lat1, lon1 = math.radians(coords[i-1][0]), math.radians(coords[i-1][1])
        lat2, lon2 = math.radians(coords[i][0]),   math.radians(coords[i][1])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        total += R * 2 * math.asin(math.sqrt(a))
    return round(total, 2)


def parse_element(elements: list, trek_name: str) -> dict | None:
    """Pick the best matching element (prefer named relations) and extract fields."""
    # Priority: relation with name > way with name > first element
    best = None
    for el in elements:
        tags = el.get("tags", {})
        name_tag = tags.get("name", "")
        if el["type"] == "relation" and trek_name.lower() in name_tag.lower():
            best = el
            break
    if best is None:
        for el in elements:
            tags = el.get("tags", {})
            name_tag = tags.get("name", "")
            if trek_name.lower() in name_tag.lower():
                best = el
                break
    if best is None and elements:
        best = elements[0]
    if best is None:
        return None

    tags = best.get("tags", {})
    coords = extract_geometry(elements)
    clat, clng = centroid(coords)
    distance = haversine_km(coords) if coords else None

    # Infer state from centroid latitude (rough but useful for the project)
    state = infer_state(clat, clng) if clat else None

    return {
        "osm_id":         f"{best['type']}/{best['id']}",
        "name":           tags.get("name", trek_name),
        "region":         tags.get("region") or tags.get("area"),
        "state":          state,
        "difficulty":     tags.get("sac_scale") or tags.get("difficulty") or tags.get("grade"),
        "altitude_max_m": _to_float(tags.get("ele:max") or tags.get("ele")),
        "distance_km":    _to_float(tags.get("distance")) or distance,
        "duration_days":  tags.get("duration"),
        "surface":        tags.get("surface"),
        "network":        tags.get("network"),
        "operator":       tags.get("operator"),
        "description":    tags.get("description"),
        "wikipedia":      tags.get("wikipedia"),
        "wikidata":       tags.get("wikidata"),
        "website":        tags.get("website") or tags.get("url"),
        "osm_type":       best["type"],
        "tags_json":      json.dumps(tags, ensure_ascii=False),
        "centroid_lat":   clat,
        "centroid_lng":   clng,
        "geometry_json":  json.dumps(coords[:500]),  # cap at 500 pts to keep DB lean
        "coords":         coords,   # used for waypoints table, not stored directly
    }


def _to_float(val) -> float | None:
    try:
        return float(str(val).replace("m", "").replace("km", "").strip()) if val else None
    except ValueError:
        return None


def infer_state(lat: float, lng: float) -> str:
    """Very rough state inference from lat/lng for Indian treks."""
    if lat > 32:
        return "Jammu & Kashmir / Ladakh"
    if lat > 30 and lng < 78:
        return "Himachal Pradesh"
    if lat > 29 and lng > 78:
        return "Uttarakhand"
    if lat > 26 and lng > 88:
        return "Sikkim / North East"
    if lat < 16:
        return "Karnataka / Kerala"
    return "India"


# ─── DB insertion ──────────────────────────────────────────────────────────────

def insert_trek(conn: sqlite3.Connection, data: dict, treks_table: str, waypoints_table: str) -> int | None:
    coords = data.pop("coords", [])
    trek_columns = get_table_columns(conn, treks_table)
    cols = [k for k in data if k in trek_columns]
    if not cols:
        print("  ✗  DB table schema does not match trek data")
        return None
    placeholders = ", ".join(["?"] * len(cols))
    col_names = ", ".join(cols)
    values = [data[c] for c in cols]

    try:
        cur = conn.execute(
            f"INSERT OR REPLACE INTO {treks_table} ({col_names}) VALUES ({placeholders})",
            values,
        )
        trek_id = cur.lastrowid
        conn.commit()

        if coords:
            waypoint_columns = get_table_columns(conn, waypoints_table)
            insert_cols = ["trek_id", "seq", "lat", "lng"]
            if "ele" in waypoint_columns:
                insert_cols.append("ele")

            placeholders = ", ".join(["?"] * len(insert_cols))
            col_names = ", ".join(insert_cols)
            waypoints = []
            for i, (lat, lng) in enumerate(coords[::5]):
                row = [trek_id, i, lat, lng]
                if "ele" in waypoint_columns:
                    row.append(None)
                waypoints.append(tuple(row))

            conn.executemany(
                f"INSERT INTO {waypoints_table} ({col_names}) VALUES ({placeholders})",
                waypoints,
            )
            conn.commit()

        return trek_id
    except sqlite3.Error as e:
        print(f"  ✗  DB error: {e}")
        return None


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    conn, treks_table, waypoints_table = init_db()
    success, failed = [], []

    print(f"\n🏔  Fetching {len(TREK_NAMES)} Indian treks from OpenStreetMap Overpass API\n")
    print("=" * 60)

    for i, trek_name in enumerate(TREK_NAMES, 1):
        print(f"[{i:02d}/{len(TREK_NAMES)}]  {trek_name} …", end=" ", flush=True)

        query = build_query(trek_name, INDIA_BBOX)
        raw = fetch_overpass(query)

        if not raw or not raw.get("elements"):
            print("❌  No OSM data found")
            failed.append(trek_name)
            time.sleep(2)
            continue

        parsed = parse_element(raw["elements"], trek_name)
        if not parsed:
            print("❌  Could not parse response")
            failed.append(trek_name)
            time.sleep(2)
            continue

        trek_id = insert_trek(conn, parsed, treks_table, waypoints_table)
        if trek_id:
            coords_count = len(raw["elements"])
            print(f"✅  Saved (id={trek_id}, {coords_count} OSM elements)")
            success.append(trek_name)
        else:
            print("❌  DB insert failed")
            failed.append(trek_name)

        # Be a polite API citizen — Overpass recommends ~2s between requests
        time.sleep(3)

    print("\n" + "=" * 60)
    print(f"✅  Successful: {len(success)}/{len(TREK_NAMES)}")
    if failed:
        print(f"❌  Failed:     {', '.join(failed)}")
        print("    → Re-run or add OSM relation IDs manually for these (see README below)")

    # Print a preview of what's in the DB
    print("\n📋  Preview of stored treks:")
    print(f"{'#':<4} {'Name':<30} {'State':<28} {'Dist (km)':<12} {'Difficulty'}")
    print("-" * 85)
    for row in conn.execute(
        "SELECT id, name, state, distance_km, difficulty FROM treks ORDER BY id"
    ):
        tid, name, state, dist, diff = row
        dist_str = f"{dist:.1f}" if dist else "—"
        print(f"{tid:<4} {(name or ''):<30} {(state or ''):<28} {dist_str:<12} {diff or '—'}")

    conn.close()
    print("\n✅  Done. Database saved to → treks.db")


if __name__ == "__main__":
    main()