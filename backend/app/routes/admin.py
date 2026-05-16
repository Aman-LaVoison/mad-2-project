from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from functools import wraps
from app.extensions import db
from app.models import User, Trek, Booking, StaffProfile

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    """Decorator to check if user is admin"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/dashboard', methods=['GET'])
@login_required
@admin_required
def get_dashboard():
    """Get admin dashboard data"""
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(user_type='user').count()
    total_staff = User.query.filter_by(user_type='staff').count()
    total_bookings = Booking.query.count()
    
    # Recent bookings
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    
    return jsonify({
        'dashboard': {
            'total_treks': total_treks,
            'total_users': total_users,
            'total_staff': total_staff,
            'total_bookings': total_bookings,
            'recent_bookings': [{
                'id': b.id,
                'user_id': b.user_id,
                'trek_id': b.trek_id,
                'status': b.booking_status,
                'date': b.booking_date.isoformat()
            } for b in recent_bookings]
        }
    }), 200

@admin_bp.route('/treks', methods=['GET'])
@login_required
@admin_required
def list_treks():
    """List all treks"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Trek.query
    
    # Filtering
    if request.args.get('status'):
        query = query.filter_by(status=request.args.get('status'))
    if request.args.get('difficulty'):
        query = query.filter_by(difficulty=request.args.get('difficulty'))
    if request.args.get('location'):
        query = query.filter(Trek.location.ilike(f"%{request.args.get('location')}%"))
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    treks = [{
        'id': t.id,
        'trek_name': t.trek_name,
        'location': t.location,
        'difficulty': t.difficulty,
        'status': t.status,
        'available_slots': t.available_slots,
        'total_slots': t.total_slots,
        'start_date': t.start_date.isoformat()
    } for t in pagination.items]
    
    return jsonify({
        'treks': treks,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@admin_bp.route('/treks', methods=['POST'])
@login_required
@admin_required
def create_trek():
    """Create a new trek"""
    data = request.get_json()
    
    required_fields = ['trek_name', 'location', 'difficulty', 'duration_days', 'total_slots', 'start_date', 'end_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    trek = Trek(
        trek_name=data['trek_name'],
        location=data['location'],
        difficulty=data['difficulty'],
        duration_days=data['duration_days'],
        total_slots=data['total_slots'],
        available_slots=data['total_slots'],
        description=data.get('description'),
        status='Pending'
    )
    
    db.session.add(trek)
    db.session.commit()
    
    return jsonify({
        'message': 'Trek created successfully',
        'trek_id': trek.id
    }), 201

@admin_bp.route('/treks/<int:trek_id>', methods=['PUT'])
@login_required
@admin_required
def update_trek(trek_id):
    """Update trek details"""
    trek = Trek.query.get_or_404(trek_id)
    data = request.get_json()
    
    # Update fields
    for field in ['trek_name', 'location', 'difficulty', 'duration_days', 'total_slots', 'status', 'description']:
        if field in data:
            setattr(trek, field, data[field])
    
    db.session.commit()
    
    return jsonify({'message': 'Trek updated successfully'}), 200

@admin_bp.route('/treks/<int:trek_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_trek(trek_id):
    """Delete a trek"""
    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()
    
    return jsonify({'message': 'Trek deleted successfully'}), 200

@admin_bp.route('/staff', methods=['GET'])
@login_required
@admin_required
def list_staff():
    """List all staff members"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    staff = User.query.filter_by(user_type='staff').paginate(page=page, per_page=per_page)
    
    staff_list = [{
        'id': s.id,
        'username': s.username,
        'email': s.email,
        'full_name': s.full_name,
        'is_active': s.is_active
    } for s in staff.items]
    
    return jsonify({
        'staff': staff_list,
        'total': staff.total,
        'pages': staff.pages,
        'current_page': page
    }), 200

@admin_bp.route('/staff', methods=['POST'])
@login_required
@admin_required
def add_staff():
    """Add new staff member"""
    data = request.get_json()
    
    required_fields = ['username', 'email', 'full_name', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    staff = User(
        username=data['username'],
        email=data['email'],
        full_name=data['full_name'],
        user_type='staff',
        is_active=True
    )
    staff.set_password(data['password'])
    
    db.session.add(staff)
    db.session.commit()
    
    return jsonify({
        'message': 'Staff member added successfully',
        'staff_id': staff.id
    }), 201

@admin_bp.route('/staff/<int:staff_id>/assign-trek/<int:trek_id>', methods=['POST'])
@login_required
@admin_required
def assign_staff_to_trek(staff_id, trek_id):
    """Assign staff to a trek"""
    staff = User.query.filter_by(id=staff_id, user_type='staff').get_or_404()
    trek = Trek.query.get_or_404(trek_id)
    
    trek.assigned_staff_id = staff_id
    db.session.commit()
    
    return jsonify({'message': 'Staff assigned to trek successfully'}), 200

@admin_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def list_users():
    """List all users"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    users = User.query.filter_by(user_type='user').paginate(page=page, per_page=per_page)
    
    users_list = [{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'full_name': u.full_name,
        'is_active': u.is_active,
        'is_blacklisted': u.is_blacklisted,
        'created_at': u.created_at.isoformat()
    } for u in users.items]
    
    return jsonify({
        'users': users_list,
        'total': users.total,
        'pages': users.pages,
        'current_page': page
    }), 200

@admin_bp.route('/users/<int:user_id>/deactivate', methods=['POST'])
@login_required
@admin_required
def deactivate_user(user_id):
    """Deactivate a user"""
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'User deactivated successfully'}), 200

@admin_bp.route('/users/<int:user_id>/blacklist', methods=['POST'])
@login_required
@admin_required
def blacklist_user(user_id):
    """Blacklist a user"""
    user = User.query.get_or_404(user_id)
    user.is_blacklisted = True
    db.session.commit()
    
    return jsonify({'message': 'User blacklisted successfully'}), 200
