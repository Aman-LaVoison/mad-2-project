from flask import Blueprint, request, jsonify
from flask_security import login_user, logout_user, current_user
from app.extensions import db
from app.models import User
from datetime import datetime
from app.extensions import db, security # Import the global security instance

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration (only for Trekkers)"""
    data = request.get_json()
    
    # Validation
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user_datastore = security.datastore
    # Create new user (default type: 'user' for trekkers)
    user = user_datastore.create_user(
        email=data['email'],
        username=data['username'],
        password_hash=data['password'], # Hash explicitly or let datastore handle it
        full_name=data.get('full_name', ''),
        active=True
    )
    
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'Registration successful. Please log in.',
        'user_id': user.id
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login for all user types"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if not user.active:
        return jsonify({'error': 'Account is inactive'}), 403
    
    if user.blacklisted:
        return jsonify({'error': 'Account is blacklisted'}), 403
    

    login_user(user)

    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': user.user_type,
            'full_name': user.full_name
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get current user profile"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'full_name': current_user.full_name,
            'phone': current_user.phone,
            'address': current_user.address,
            'date_of_birth': current_user.date_of_birth.isoformat() if current_user.date_of_birth else None,
            'user_type': current_user.user_type,
            'profile_completed': current_user.profile_completed,
            'created_at': current_user.created_at.isoformat()
        }
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
def update_profile():
    """Update user profile"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    # Update allowed fields
    if 'full_name' in data:
        current_user.full_name = data['full_name']
    if 'phone' in data:
        current_user.phone = data['phone']
    if 'address' in data:
        current_user.address = data['address']
    if 'date_of_birth' in data:
        current_user.date_of_birth = data['date_of_birth']
    
    current_user.profile_completed = True
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'full_name': current_user.full_name,
            'phone': current_user.phone,
            'address': current_user.address
        }
    }), 200
