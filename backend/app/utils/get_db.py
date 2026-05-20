import sqlite3, json, os

# Point the DB to the project's instance folder (../.. /instance/trekking_app.db)
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'trekking_app.db'))

def getdb():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
