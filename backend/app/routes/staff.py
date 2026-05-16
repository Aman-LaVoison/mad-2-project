from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from functools import wraps
from app.extensions import db
from app.models import User, Trek, Booking
from datetime import datetime

staff_bp = Blueprint('staff', __name__)

def staff_required(fn):
    """Decorator to check if user is staff"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'staff':
            return jsonify({'error': 'Staff access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@staff_bp.route('/dashboard', methods=['GET'])
@login_required
@staff_required
def get_dashboard():
    """Get staff dashboard"""
    # Get treks assigned to this staff
    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_user.id).all()
    
    trek_stats = []
    total_participants = 0
    
    for trek in assigned_treks:
        bookings = Booking.query.filter_by(trek_id=trek.id, booking_status='Booked').count()
        total_participants += bookings
        
        trek_stats.append({
            'id': trek.id,
            'trek_name': trek.trek_name,
            'location': trek.location,
            'status': trek.status,
            'participants': bookings,
            'available_slots': trek.available_slots,
            'start_date': trek.start_date.isoformat()
        })
    
    return jsonify({
        'dashboard': {
            'assigned_treks_count': len(assigned_treks),
            'total_participants': total_participants,
            'treks': trek_stats
        }
    }), 200

@staff_bp.route('/my-treks', methods=['GET'])
@login_required
@staff_required
def get_my_treks():
    """Get treks assigned to current staff"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    treks = Trek.query.filter_by(assigned_staff_id=current_user.id).paginate(page=page, per_page=per_page)
    
    trek_list = [{
        'id': t.id,
        'trek_name': t.trek_name,
        'location': t.location,
        'difficulty': t.difficulty,
        'status': t.status,
        'available_slots': t.available_slots,
        'total_slots': t.total_slots,
        'start_date': t.start_date.isoformat(),
        'end_date': t.end_date.isoformat()
    } for t in treks.items]
    
    return jsonify({
        'treks': trek_list,
        'total': treks.total,
        'pages': treks.pages,
        'current_page': page
    }), 200

@staff_bp.route('/treks/<int:trek_id>/participants', methods=['GET'])
@login_required
@staff_required
def get_trek_participants(trek_id):
    """Get list of participants for a trek"""
    trek = Trek.query.get_or_404(trek_id)
    
    # Verify staff is assigned to this trek
    if trek.assigned_staff_id != current_user.id:
        return jsonify({'error': 'Not authorized to view this trek'}), 403
    
    bookings = Booking.query.filter_by(trek_id=trek_id, booking_status='Booked').all()
    
    participants = [{
        'id': b.id,
        'user_id': b.user_id,
        'user_name': b.user.full_name,
        'user_email': b.user.email,
        'booking_date': b.booking_date.isoformat(),
        'status': b.booking_status
    } for b in bookings]
    
    return jsonify({
        'trek_id': trek_id,
        'trek_name': trek.trek_name,
        'total_participants': len(participants),
        'participants': participants
    }), 200

@staff_bp.route('/treks/<int:trek_id>/update-status', methods=['PUT'])
@login_required
@staff_required
def update_trek_status(trek_id):
    """Update trek status"""
    trek = Trek.query.get_or_404(trek_id)
    
    # Verify staff is assigned to this trek
    if trek.assigned_staff_id != current_user.id:
        return jsonify({'error': 'Not authorized to update this trek'}), 403
    
    data = request.get_json()
    
    if 'status' in data:
        trek.status = data['status']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Trek status updated successfully',
        'trek_id': trek_id,
        'status': trek.status
    }), 200

@staff_bp.route('/treks/<int:trek_id>/update-slots', methods=['PUT'])
@login_required
@staff_required
def update_trek_slots(trek_id):
    """Update available slots for a trek"""
    trek = Trek.query.get_or_404(trek_id)
    
    # Verify staff is assigned to this trek
    if trek.assigned_staff_id != current_user.id:
        return jsonify({'error': 'Not authorized to update this trek'}), 403
    
    data = request.get_json()
    
    if 'available_slots' in data:
        available_slots = data['available_slots']
        if available_slots < 0 or available_slots > trek.total_slots:
            return jsonify({'error': 'Invalid number of slots'}), 400
        trek.available_slots = available_slots
    
    db.session.commit()
    
    return jsonify({
        'message': 'Slots updated successfully',
        'available_slots': trek.available_slots
    }), 200
