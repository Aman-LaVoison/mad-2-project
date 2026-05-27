from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from celery import Celery
import redis
from flask_security import Security

db = SQLAlchemy()
login_manager = LoginManager()
cors = CORS()
security = Security()
# Redis client
redis_client = None

# Celery app
celery_app = Celery(__name__)

def init_redis(app):
    """Initialize Redis connection"""
    global redis_client
    redis_client = redis.Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'],
        decode_responses=True
    )
    return redis_client

def init_celery(app):
    """Initialize Celery with Flask app"""
    celery_app.conf.update(app.config)
    
    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery_app.Task = ContextTask
    return celery_app
