from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from app.extensions import db


# Association table for many-to-many relationship
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    """Role model for defining user roles."""
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(255))
    name = db.Column(db.String(80), unique=True)


class User(UserMixin, db.Model):

    """User model for all user types (Admin, Staff, Trekker)"""

    __tablename__ = 'user'
    
    active = db.Column(db.Boolean, default=True)
    address = db.Column(db.String(255))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    gender = db.Column(db.String(20))
    nationality = db.Column(db.String(80))
    company_or_college = db.Column(db.String(120))
    designation_or_course = db.Column(db.String(120))
    pin_code = db.Column(db.String(20))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    country = db.Column(db.String(80))
    height_cm = db.Column(db.Integer)
    weight_kg = db.Column(db.Integer)
    emergency_contact = db.Column(db.String(50))
    emergency_email = db.Column(db.String(120))
    emergency_contact_name = db.Column(db.String(120))
    emergency_relationship = db.Column(db.String(80))
    food_preference = db.Column(db.String(80))
    food_allergies = db.Column(db.String(255))
    tshirt_size = db.Column(db.String(20))
    shoe_size = db.Column(db.String(20))
    blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    fs_uniquifier = db.Column(db.String(64), unique=True)  # Flask-Security requirement
    full_name = db.Column(db.String(120), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    profile_completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_type = db.Column(db.String(20), nullable=False, default='user', index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    
    current_login_at = db.Column(db.DateTime, default=datetime.utcnow)
    current_login_ip = db.Column(db.String(100))
    last_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer, default=0)


    # Relationships
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    wishlists = db.relationship('Wishlist', backref='user', lazy=True, cascade='all, delete-orphan')
    vouchers = db.relationship('Voucher', backref='user', lazy=True, cascade='all, delete-orphan')
    staff_profile = db.relationship('StaffProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Trek(db.Model):

    """Trek/Trekking route model"""
    __tablename__ = 'treks'
    
    accommodation = db.Column(db.Text)
    altitude = db.Column(db.String(100))
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    available_slots = db.Column(db.Integer, nullable=False)
    best_season = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy, Moderate, Hard
    duration_days = db.Column(db.Integer, nullable=False)  # Duration in days
    end_date = db.Column(db.DateTime, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    itinerary = db.Column(db.Text)
    location = db.Column(db.String(150), nullable=False, index=True)
    price = db.Column(db.Float)
    registration_deadline = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending', index=True)
    total_slots = db.Column(db.Integer, nullable=False)
    trek_name = db.Column(db.String(150), nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Staff assignment
    assigned_staff = db.relationship('User', backref='assigned_treks')
    
    # Relationships
    bookings = db.relationship('Booking', backref='trek', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Trek {self.trek_name}>'


class Booking(db.Model):
    """Booking model - records of user trek bookings"""
    __tablename__ = 'bookings'
    
    amount_paid = db.Column(db.Float)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    booking_status = db.Column(db.String(20), nullable=False, default='Booked')
    cancellation_date = db.Column(db.DateTime)
    cancellation_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(50))  # Card, UPI, Cash, etc.
    payment_status = db.Column(db.String(20), default='Pending')
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    
    def __repr__(self):
        return f'<Booking User:{self.user_id} Trek:{self.trek_id}>'


class Wishlist(db.Model):
    """Wishlist for user trek favorites"""
    __tablename__ = 'wishlists'

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

    trek = db.relationship('Trek', backref='wishlists')

    def __repr__(self):
        return f'<Wishlist User:{self.user_id} Trek:{self.trek_id}>'


class Voucher(db.Model):
    """Vouchers that users can apply to trek bookings"""
    __tablename__ = 'vouchers'

    code = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255))
    discount = db.Column(db.Float, default=0.0)
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='active')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    valid_from = db.Column(db.DateTime)
    valid_until = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Voucher {self.code} User:{self.user_id}>'


class StaffProfile(db.Model):
    """Trek Staff profile"""
    __tablename__ = 'staff_profiles'
    
    active = db.Column(db.Boolean, default=True)
    certifications = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    designation = db.Column(db.String(100))
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    experience_years = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<StaffProfile {self.employee_id}>'


class AuditLog(db.Model):
    """Audit log for tracking admin actions"""
    __tablename__ = 'audit_logs'
    
    action = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    details = db.Column(db.Text)
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50))
    resource_id = db.Column(db.Integer)
    resource_type = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<AuditLog {self.action}>'
