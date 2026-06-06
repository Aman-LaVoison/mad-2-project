from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from functools import wraps
from sqlalchemy import or_
from app.extensions import db
from app.models import User, Trek, Booking, Wishlist, Voucher
from datetime import datetime

import json
user_bp = Blueprint('user', __name__)

def user_required(fn):
    """Decorator to check if user is a trekker"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'user':
            return jsonify({'error': 'User access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@user_bp.route('/dashboard', methods=['GET'])
@login_required
@user_required
def get_dashboard():
    """Get user dashboard"""
    # Get user's bookings
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    
    booked_count = sum(1 for b in bookings if b.booking_status == 'Booked')
    completed_count = sum(1 for b in bookings if b.booking_status == 'Completed')
    cancelled_count = sum(1 for b in bookings if b.booking_status == 'Cancelled')
    
    return jsonify({
        'dashboard': {
            'total_bookings': len(bookings),
            'booked_treks': booked_count,
            'completed_treks': completed_count,
            'cancelled_bookings': cancelled_count,
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email,
                'full_name': current_user.full_name
            }
        }
    }), 200


@user_bp.route('/dashboard/profile', methods=['GET'])
@login_required
@user_required
def get_dashboard_profile():
    """Get current user dashboard profile"""
    return jsonify({
        'profile': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'full_name': current_user.full_name,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'phone': current_user.phone,
            'address': current_user.address,
            'date_of_birth': current_user.date_of_birth.isoformat() if current_user.date_of_birth else None,
            'gender': current_user.gender,
            'nationality': current_user.nationality,
            'company_or_college': current_user.company_or_college,
            'designation_or_course': current_user.designation_or_course,
            'pin_code': current_user.pin_code,
            'city': current_user.city,
            'state': current_user.state,
            'country': current_user.country,
            'height_cm': current_user.height_cm,
            'weight_kg': current_user.weight_kg,
            'emergency_contact_name': current_user.emergency_contact_name,
            'emergency_contact': current_user.emergency_contact,
            'emergency_email': current_user.emergency_email,
            'emergency_relationship': current_user.emergency_relationship,
            'food_preference': current_user.food_preference,
            'food_allergies': current_user.food_allergies,
            'tshirt_size': current_user.tshirt_size,
            'shoe_size': current_user.shoe_size,
            'profile_completed': current_user.profile_completed,
            'created_at': current_user.created_at.isoformat() if current_user.created_at else None
        }
    }), 200


@user_bp.route('/dashboard/profile', methods=['PUT'])
@login_required
@user_required
def update_dashboard_profile():
    """Update current user dashboard profile"""
    data = request.get_json() or {}

    for field in [
        'full_name', 'first_name', 'last_name', 'phone', 'address', 'date_of_birth',
        'gender', 'nationality', 'company_or_college', 'designation_or_course',
        'pin_code', 'city', 'state', 'country', 'height_cm', 'weight_kg',
        'emergency_contact_name', 'emergency_contact', 'emergency_email',
        'emergency_relationship', 'food_preference', 'food_allergies',
        'tshirt_size', 'shoe_size'
    ]:
        if field in data:
            setattr(current_user, field, data[field])

    current_user.profile_completed = True
    db.session.commit()

    return jsonify({'message': 'Profile updated successfully'}), 200


@user_bp.route('/dashboard/upcoming-treks', methods=['GET'])
@login_required
@user_required
def get_upcoming_treks():
    """Get upcoming treks for current user"""
    now = datetime.utcnow()
    bookings = Booking.query.filter_by(user_id=current_user.id, booking_status='Booked').join(Trek).filter(Trek.start_date >= now).all()

    treks = [{
        'id': b.trek.id,
        'trek_name': b.trek.trek_name,
        'location': b.trek.location,
        'difficulty': b.trek.difficulty,
        'duration_days': b.trek.duration_days,
        'start_date': b.trek.start_date.isoformat(),
        'end_date': b.trek.end_date.isoformat(),
        'booking_status': b.booking_status,
        'payment_status': b.payment_status,
        'available_slots': b.trek.available_slots,
        'total_slots': b.trek.total_slots,
        'price': b.trek.price,
        'description': b.trek.description
    } for b in bookings]

    return jsonify({'upcoming_treks': treks, 'total': len(treks)}), 200


@user_bp.route('/dashboard/previous-treks', methods=['GET'])
@login_required
@user_required
def get_previous_treks():
    """Get previous treks for current user"""
    now = datetime.utcnow()
    bookings = Booking.query.filter_by(user_id=current_user.id).join(Trek).filter(
        or_(Booking.booking_status == 'Completed', Trek.end_date < now)
    ).all()

    treks = [{
        'id': b.trek.id,
        'trek_name': b.trek.trek_name,
        'location': b.trek.location,
        'difficulty': b.trek.difficulty,
        'duration_days': b.trek.duration_days,
        'start_date': b.trek.start_date.isoformat(),
        'end_date': b.trek.end_date.isoformat(),
        'booking_status': b.booking_status,
        'payment_status': b.payment_status,
        'price': b.trek.price,
        'description': b.trek.description
    } for b in bookings]

    return jsonify({'previous_treks': treks, 'total': len(treks)}), 200


@user_bp.route('/dashboard/wishlist', methods=['GET'])
@login_required
@user_required
def get_user_wishlist():
    """Get the current user's wishlist"""
    items = Wishlist.query.filter_by(user_id=current_user.id).join(Trek).all()

    wishlist = [{
        'id': item.id,
        'trek_id': item.trek_id,
        'trek_name': item.trek.trek_name,
        'location': item.trek.location,
        'start_date': item.trek.start_date.isoformat(),
        'price': item.trek.price,
        'description': item.trek.description
    } for item in items]

    return jsonify({'wishlist': wishlist, 'total': len(wishlist)}), 200


@user_bp.route('/dashboard/vouchers', methods=['GET'])
@login_required
@user_required
def get_user_vouchers():
    """Get the current user's vouchers"""
    vouchers = Voucher.query.filter_by(user_id=current_user.id).all()

    items = [{
        'id': v.id,
        'code': v.code,
        'description': v.description,
        'discount': v.discount,
        'status': v.status,
        'valid_from': v.valid_from.isoformat() if v.valid_from else None,
        'valid_until': v.valid_until.isoformat() if v.valid_until else None
    } for v in vouchers]

    return jsonify({'vouchers': items, 'total': len(items)}), 200


@user_bp.route('/available-treks', methods=['GET'])
@login_required
@user_required
def list_available_treks():
    """List available treks for booking"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Trek.query.filter(Trek.status.in_(['Open', 'Approved']))
    query = query.filter(Trek.available_slots > 0)
    
    # Filtering
    if request.args.get('difficulty'):
        query = query.filter_by(difficulty=request.args.get('difficulty'))
    if request.args.get('location'):
        query = query.filter(Trek.location.ilike(f"%{request.args.get('location')}%"))
    if request.args.get('duration_min'):
        query = query.filter(Trek.duration_days >= int(request.args.get('duration_min')))
    if request.args.get('duration_max'):
        query = query.filter(Trek.duration_days <= int(request.args.get('duration_max')))
    
    # Sorting
    sort_by = request.args.get('sort_by', 'start_date')
    if sort_by == 'start_date':
        query = query.order_by(Trek.start_date.asc())
    elif sort_by == 'difficulty':
        query = query.order_by(Trek.difficulty.asc())
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    treks = [{
        'id': t.id,
        'trek_name': t.trek_name,
        'location': t.location,
        'difficulty': t.difficulty,
        'duration_days': t.duration_days,
        'available_slots': t.available_slots,
        'total_slots': t.total_slots,
        'start_date': t.start_date.isoformat(),
        'end_date': t.end_date.isoformat(),
        'price': t.price,
        'description': t.description
    } for t in pagination.items]
    
    return jsonify({
        'treks': treks,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@user_bp.route('/treks/<int:trek_id>', methods=['GET'])
@login_required
@user_required
def get_trek_details(trek_id):
    """Get detailed information about a trek"""
    trek = Trek.query.get_or_404(trek_id)
    
    # Check if user already booked this trek
    user_booking = Booking.query.filter_by(user_id=current_user.id, trek_id=trek_id).first()
    
    return jsonify({
        'trek': {
            'id': trek.id,
            'trek_name': trek.trek_name,
            'location': trek.location,
            'description': trek.description,
            'difficulty': trek.difficulty,
            'duration_days': trek.duration_days,
            'altitude': trek.altitude,
            'best_season': trek.best_season,
            'accommodation': trek.accommodation,
            'itinerary': trek.itinerary,
            'price': trek.price,
            'available_slots': trek.available_slots,
            'total_slots': trek.total_slots,
            'start_date': trek.start_date.isoformat(),
            'end_date': trek.end_date.isoformat(),
            'status': trek.status,
            'is_booked_by_user': bool(user_booking),
            'booking_status': user_booking.booking_status if user_booking else None
        }
    }), 200

@user_bp.route('/book-trek', methods=['POST'])
@login_required
@user_required
def book_trek():
    """Book a trek"""
    data = request.get_json()
    
    if not data or 'trek_id' not in data:
        return jsonify({'error': 'Trek ID required'}), 400
    
    trek = Trek.query.get_or_404(data['trek_id'])
    
    # Validation
    if trek.status != 'Open':
        return jsonify({'error': 'Trek is not open for bookings'}), 400
    
    if trek.available_slots <= 0:
        return jsonify({'error': 'No slots available'}), 400
    
    # Check if user already booked this trek
    existing_booking = Booking.query.filter_by(user_id=current_user.id, trek_id=trek.id).first()
    if existing_booking and existing_booking.booking_status == 'Booked':
        return jsonify({'error': 'You have already booked this trek'}), 400
    
    # Create booking
    booking = Booking(
        user_id=current_user.id,
        trek_id=trek.id,
        booking_status='Booked',
        payment_status='Pending'
    )
    
    # Update available slots
    trek.available_slots -= 1
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({
        'message': 'Trek booked successfully',
        'booking_id': booking.id,
        'booking_status': booking.booking_status
    }), 201

@user_bp.route('/bookings', methods=['GET'])
@login_required
@user_required
def get_user_bookings():
    """Get all bookings for current user"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    bookings = Booking.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=per_page)
    
    booking_list = [{
        'id': b.id,
        'trek_id': b.trek_id,
        'trek_name': b.trek.trek_name,
        'location': b.trek.location,
        'start_date': b.trek.start_date.isoformat(),
        'end_date': b.trek.end_date.isoformat(),
        'booking_status': b.booking_status,
        'payment_status': b.payment_status,
        'booking_date': b.booking_date.isoformat()
    } for b in bookings.items]
    
    return jsonify({
        'bookings': booking_list,
        'total': bookings.total,
        'pages': bookings.pages,
        'current_page': page
    }), 200

@user_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
@user_required
def cancel_booking(booking_id):
    """Cancel a booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Verify ownership
    if booking.user_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403
    
    if booking.booking_status != 'Booked':
        return jsonify({'error': 'Can only cancel booked treks'}), 400
    
    data = request.get_json() or {}
    
    booking.booking_status = 'Cancelled'
    booking.cancellation_date = datetime.utcnow()
    booking.cancellation_reason = data.get('reason', '')
    
    # Restore available slots
    booking.trek.available_slots += 1
    
    db.session.commit()
    
    return jsonify({
        'message': 'Booking cancelled successfully'
    }), 200

@user_bp.route('/booking-history', methods=['GET'])
@login_required
@user_required
def get_booking_history():
    """Get user's complete booking history"""
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    
    history = [{
        'id': b.id,
        'trek_id': b.trek_id,
        'trek_name': b.trek.trek_name,
        'location': b.trek.location,
        'difficulty': b.trek.difficulty,
        'duration_days': b.trek.duration_days,
        'start_date': b.trek.start_date.isoformat(),
        'end_date': b.trek.end_date.isoformat(),
        'booking_date': b.booking_date.isoformat(),
        'booking_status': b.booking_status,
        'payment_status': b.payment_status
    } for b in bookings]
    
    return jsonify({
        'booking_history': history,
        'total_bookings': len(history)
    }), 200

@user_bp.route('/export-booking-history', methods=['POST'])
@login_required
@user_required
def export_booking_history():
    """Trigger async job to export booking history as CSV"""
    # This will trigger a Celery task
    from app.tasks import export_user_booking_csv
    
    task = export_user_booking_csv.delay(current_user.id)
    
    return jsonify({
        'message': 'Export job triggered. You will receive a notification when ready.',
        'task_id': task.id
    }), 202

@user_bp.route('/search-treks', methods=['GET'])
@login_required
@user_required
def search_treks():
    """Search for treks with multiple filters"""
    query = Trek.query.filter(Trek.status.in_(['Open', 'Approved']))
    query = query.filter(Trek.available_slots > 0)
    
    # Multi-field search
    search_term = request.args.get('q', '')
    if search_term:
        query = query.filter(
            (Trek.trek_name.ilike(f"%{search_term}%")) |
            (Trek.location.ilike(f"%{search_term}%")) |
            (Trek.description.ilike(f"%{search_term}%"))
        )
    
    # Advanced filters
    if request.args.get('difficulty'):
        query = query.filter(Trek.difficulty == request.args.get('difficulty'))
    if request.args.get('min_price'):
        query = query.filter(Trek.price >= float(request.args.get('min_price')))
    if request.args.get('max_price'):
        query = query.filter(Trek.price <= float(request.args.get('max_price')))
    if request.args.get('min_duration'):
        query = query.filter(Trek.duration_days >= int(request.args.get('min_duration')))
    if request.args.get('max_duration'):
        query = query.filter(Trek.duration_days <= int(request.args.get('max_duration')))
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    treks = [{
        'id': t.id,
        'trek_name': t.trek_name,
        'location': t.location,
        'difficulty': t.difficulty,
        'duration_days': t.duration_days,
        'price': t.price,
        'start_date': t.start_date.isoformat()
    } for t in pagination.items]
    
    return jsonify({
        'treks': treks,
        'total': pagination.total,
        'pages': pagination.pages
    }), 200


 
@user_bp.route("/api/treks", methods=["GET"])
def get_treks():
    """
    GET /api/treks
    Optional query params:
      ?state=Uttarakhand
      ?difficulty=hiking
      ?search=roopkund
    """
    state      = request.args.get("state")
    difficulty = request.args.get("difficulty")
    search     = request.args.get("search")
 
    sql    = "SELECT * FROM treks WHERE 1=1"
    params = []
 
    if state:
        sql += " AND state LIKE ?"
        params.append(f"%{state}%")
    if difficulty:
        sql += " AND difficulty = ?"
        params.append(difficulty)
    if search:
        sql += " AND name LIKE ?"
        params.append(f"%{search}%")
 
    sql += " ORDER BY name"
 
    conn = get_db()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
 
    treks = []
    for row in rows:
        t = dict(row)
        # Parse JSON fields back to objects for the frontend
        t["tags"]     = json.loads(t["tags_json"] or "{}")
        t["geometry"] = json.loads(t["geometry_json"] or "[]")
        del t["tags_json"]
        del t["geometry_json"]
        treks.append(t)
 
    return jsonify({"count": len(treks), "treks": treks})
 
 
@user_bp.route("/api/treks/<int:trek_id>", methods=["GET"])
def get_trek(trek_id):
    """GET /api/treks/5  — single trek with waypoints"""
    conn  = get_db()
    row   = conn.execute("SELECT * FROM treks WHERE id = ?", (trek_id,)).fetchone()
 
    if not row:
        return jsonify({"error": "Not found"}), 404
 
    trek = dict(row)
    trek["tags"]     = json.loads(trek["tags_json"] or "{}")
    trek["geometry"] = json.loads(trek["geometry_json"] or "[]")
    del trek["tags_json"]
    del trek["geometry_json"]
 
    waypoints = conn.execute(
        "SELECT seq, lat, lng, ele FROM trek_waypoints WHERE trek_id = ? ORDER BY seq",
        (trek_id,)
    ).fetchall()
    trek["waypoints"] = [dict(w) for w in waypoints]
 
    conn.close()
    return jsonify(trek)
 
 
@user_bp.route("/api/states", methods=["GET"])
def get_states():
    """GET /api/states  — distinct states for filter dropdown"""
    conn  = get_db()
    rows  = conn.execute("SELECT DISTINCT state FROM treks WHERE state IS NOT NULL ORDER BY state").fetchall()
    conn.close()
    return jsonify([r["state"] for r in rows])