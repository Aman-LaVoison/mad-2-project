# Trekking Management Application - Project Setup Guide

## Project Structure

```
mad 2 project/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── extensions.py         # Flask extensions (DB, JWT, etc)
│   │   ├── models/
│   │   │   └── __init__.py      # Database models (User, Trek, Booking, etc)
│   │   ├── routes/
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── admin.py         # Admin routes
│   │   │   ├── staff.py         # Staff routes
│   │   │   └── user.py          # User/Trekker routes
│   │   ├── schemas/             # Request/Response schemas
│   │   ├── utils/               # Utility functions
│   │   └── tasks.py             # Celery tasks for batch jobs
│   ├── config.py                # Configuration management
│   ├── run.py                   # Flask app entry point
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── main.js             # Vue app entry point
│   │   ├── App.vue             # Root component
│   │   ├── router/
│   │   │   └── index.js        # Vue Router configuration
│   │   ├── store/
│   │   │   └── auth.js         # Pinia auth store
│   │   ├── services/
│   │   │   └── api.js          # Axios API client
│   │   ├── views/              # Page components
│   │   │   ├── HomeView.vue
│   │   │   ├── auth/
│   │   │   │   ├── LoginView.vue
│   │   │   │   └── RegisterView.vue
│   │   │   ├── user/           # User dashboard, treks, bookings, profile
│   │   │   ├── admin/          # Admin dashboard, treks, staff, users
│   │   │   └── staff/          # Staff dashboard, treks, participants
│   │   ├── components/         # Reusable components
│   │   └── style.css           # Global styles
│   ├── index.html              # HTML entry point
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   └── .gitignore
│
└── README.md                    # This file
```

## Backend Setup

### Prerequisites
- Python 3.8+
- Redis (for caching and Celery)
- SQLite3

### Installation Steps

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database (automatic on first run):**
   ```bash
   python run.py
   ```
   The application will create all tables and a default admin user automatically.

6. **Run Flask development server:**
   ```bash
   python run.py
   ```
   Server will run on `http://localhost:5000`

### Default Admin Credentials
- **Username:** admin
- **Password:** admin123

## Frontend Setup

### Prerequisites
- Node.js 16+ and npm

### Installation Steps

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   Application will run on `http://localhost:3000`

4. **Build for production:**
   ```bash
   npm run build
   ```

## Running Celery (Background Jobs)

### Prerequisites
- Redis server running on localhost:6379

### Start Celery Worker:
```bash
cd backend
celery -A app.tasks worker --loglevel=info
```

### Schedule Periodic Tasks:
```bash
celery -A app.tasks beat --loglevel=info
```

## API Endpoints Overview

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Admin Routes (`/api/admin/`)
- `GET /dashboard` - Admin dashboard stats
- `GET /treks` - List all treks
- `POST /treks` - Create new trek
- `PUT /treks/<id>` - Update trek
- `DELETE /treks/<id>` - Delete trek
- `GET /staff` - List staff
- `POST /staff` - Add staff member
- `POST /staff/<id>/assign-trek/<trek_id>` - Assign staff to trek
- `GET /users` - List users
- `POST /users/<id>/deactivate` - Deactivate user
- `POST /users/<id>/blacklist` - Blacklist user

### Staff Routes (`/api/staff/`)
- `GET /dashboard` - Staff dashboard
- `GET /my-treks` - Get assigned treks
- `GET /treks/<id>/participants` - View trek participants
- `PUT /treks/<id>/update-status` - Update trek status
- `PUT /treks/<id>/update-slots` - Update available slots

### User Routes (`/api/user/`)
- `GET /dashboard` - User dashboard
- `GET /available-treks` - List available treks with filtering
- `GET /treks/<id>` - Trek details
- `POST /book-trek` - Book a trek
- `GET /bookings` - User's bookings
- `POST /bookings/<id>/cancel` - Cancel booking
- `GET /booking-history` - Complete booking history
- `POST /export-booking-history` - Export bookings as CSV
- `GET /search-treks` - Advanced trek search

## Database Models

### User
- Unified user model for Admin, Staff, and Trekkers
- Fields: username, email, password_hash, full_name, phone, address, user_type, is_active, is_blacklisted

### Trek
- Trek name, location, difficulty, duration, slots, status
- Start/end dates, assigned staff
- Description, altitude, season, accommodation, itinerary, price

### Booking
- User ID, Trek ID, booking status, payment status
- Booking dates, cancellation details

### StaffProfile
- Employee ID, designation, experience, certifications

### AuditLog
- Track admin actions for compliance

## Features Implemented

### Authentication & Authorization
- ✅ User registration and login
- ✅ Admin pre-created programmatically
- ✅ Staff access (created by admin only)
- ✅ JWT token-based authentication
- ✅ Role-based access control

### Admin Panel
- ✅ Dashboard with statistics
- ✅ Trek management (CRUD)
- ✅ Staff management
- ✅ User management
- ✅ Deactivate/blacklist users

### Trek Staff Dashboard
- ✅ View assigned treks
- ✅ View participants per trek
- ✅ Update trek status and slots
- ✅ Manage participant details

### User Dashboard
- ✅ View available treks
- ✅ Search and filter treks
- ✅ Book treks
- ✅ View bookings and history
- ✅ Cancel bookings

### Backend Jobs (Celery)
- ✅ Daily trek reminders
- ✅ Monthly activity reports
- ✅ CSV export of booking history

### Caching & Performance
- ✅ Redis integration
- ✅ Cache expiry configuration

## Next Steps for Development

1. **Implement full UI components** - Details views with forms
2. **Add pagination** - For large data sets
3. **Email notifications** - Integrate with email service
4. **Payment integration** - Basic payment simulation
5. **Charts & Analytics** - Using ChartJS
6. **PDF reports** - For monthly activity reports
7. **Mobile responsiveness** - Optimize for mobile
8. **Error handling** - Comprehensive error messages
9. **Testing** - Unit and integration tests
10. **Deployment** - Docker setup, production configuration

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
python run.py --port 5001
```

### Redis Connection Error
Ensure Redis is running:
```bash
redis-server
```

### Database Issues
Delete the database and restart:
```bash
rm backend/trekking_app.db
python backend/run.py
```

## Support & Documentation

- Flask: https://flask.palletsprojects.com/
- Vue 3: https://vuejs.org/
- SQLAlchemy: https://www.sqlalchemy.org/
- Celery: https://docs.celeryproject.org/
- Bootstrap: https://getbootstrap.com/

