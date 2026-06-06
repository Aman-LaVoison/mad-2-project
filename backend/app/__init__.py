from flask import Flask, jsonify
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore
from config import config
from app.extensions import db, login_manager, init_redis, init_celery,security,migrate
from app.models import User
import os

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db) # Initialize migration
    from app.models import User, Role  # Import models after db initialization
    login_manager.init_app(app)
    
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    CORS(app, resources={r'/api/*': {'origins': 'http://localhost:3000'}}, supports_credentials=True)
    
    # Initialize Redis
    with app.app_context():
        init_redis(app)
        init_celery(app)
    
    # Database initialization
    @app.before_request
    def init_db():
        db.create_all()
        # Create default admin if not exists
        if config_name != 'testing':
            create_default_admin()
    
    # Login manager configuration
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.staff import staff_bp
    from app.routes.user import user_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(staff_bp, url_prefix='/api/staff')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Access forbidden'}), 403
    
    # Health check
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy'}), 200
    
    return app

def create_default_admin():
    """Create default admin user"""
    existing_admin = User.query.filter_by(user_type='admin').first()
    if not existing_admin:
        
        admin = User(
            username='admin',
            email='admin@trekking-app.com',
            full_name='Administrator',
            user_type='admin',
            active=True,
            profile_completed=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created!")

if __name__ == '__main__':
    
    app = create_app()
    app.run(debug=True)
