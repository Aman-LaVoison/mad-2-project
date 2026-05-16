#!/usr/bin/env python
import os
import sys
from app import create_app, db

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    with app.app_context():
        # Create tables
        db.create_all()
        print("Database initialized!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
