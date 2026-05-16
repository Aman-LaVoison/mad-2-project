from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.extensions import db

class User(UserMixin, db.Model):
    """User model for all user types (Admin, Staff, Trekker)"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    
    # User type: admin, staff, user
    user_type = db.Column(db.String(20), nullable=False, default='user', index=True)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)
    
    # Profile completion
    profile_completed = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
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
    
    id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text)
    location = db.Column(db.String(150), nullable=False, index=True)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy, Moderate, Hard
    duration_days = db.Column(db.Integer, nullable=False)  # Duration in days
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    
    # Dates
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    registration_deadline = db.Column(db.DateTime)
    
    # Status: Pending, Approved, Open, Closed, Completed
    status = db.Column(db.String(20), nullable=False, default='Pending', index=True)
    
    # Staff assignment
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_staff = db.relationship('User', backref='assigned_treks')
    
    # Trek details
    altitude = db.Column(db.String(100))
    best_season = db.Column(db.String(100))
    accommodation = db.Column(db.Text)
    itinerary = db.Column(db.Text)
    price = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='trek', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Trek {self.trek_name}>'


class Booking(db.Model):
    """Booking model - records of user trek bookings"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False, index=True)
    
    # Booking status: Booked, Cancelled, Completed
    booking_status = db.Column(db.String(20), nullable=False, default='Booked')
    
    # Payment status: Pending, Completed, Failed
    payment_status = db.Column(db.String(20), default='Pending')
    
    # Booking details
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    cancellation_date = db.Column(db.DateTime)
    cancellation_reason = db.Column(db.Text)
    
    # Payment
    amount_paid = db.Column(db.Float)
    payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(50))  # Card, UPI, Cash, etc.
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Booking User:{self.user_id} Trek:{self.trek_id}>'


class StaffProfile(db.Model):
    """Trek Staff profile"""
    __tablename__ = 'staff_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Staff details
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    designation = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    certifications = db.Column(db.Text)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<StaffProfile {self.employee_id}>'


class AuditLog(db.Model):
    """Audit log for tracking admin actions"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(255), nullable=False)
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<AuditLog {self.action}>'
