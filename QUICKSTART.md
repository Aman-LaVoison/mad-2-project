# Quick Start Guide - Trekking Management Application

## Initial Setup (First Time)

### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional - has defaults)
cp .env.example .env

# Run the application
python run.py
```

✅ **Backend running on:** http://localhost:5000

**Default Admin Login:**
- Username: `admin`
- Password: `admin123`

### 2. Frontend Setup (New Terminal)
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ **Frontend running on:** http://localhost:3000

---

## Testing the Application

### 1. Login as Admin
1. Go to http://localhost:3000
2. Click **Login**
3. Enter:
   - Username: `admin`
   - Password: `admin123`
4. You'll see the Admin Dashboard

### 2. Create a New Trek (Admin)
- Navigate to **Admin Dashboard** → **Manage Treks**
- Click **Create Trek**
- Fill in the form with trek details
- Save

### 3. Add Trek Staff (Admin)
- Go to **Admin Dashboard** → **Manage Staff**
- Click **Add Staff Member**
- Staff can then log in and manage assigned treks

### 4. Register as User
1. Go to http://localhost:3000
2. Click **Register**
3. Fill in your details
4. Login with your new account
5. Browse and book available treks

---

## Key Features to Try

### As Admin:
- ✅ View dashboard statistics
- ✅ Create, edit, delete treks
- ✅ Add and manage staff
- ✅ Assign staff to treks
- ✅ View all users and bookings
- ✅ Deactivate or blacklist users

### As Trek Staff:
- ✅ View assigned treks
- ✅ View list of participants
- ✅ Update trek slots availability
- ✅ Update trek status (Open/Closed/Completed)

### As User/Trekker:
- ✅ View available treks
- ✅ Search and filter treks (by difficulty, location, duration)
- ✅ Book a trek
- ✅ View booking status
- ✅ Cancel bookings
- ✅ View trekking history
- ✅ Update profile

---

## API Testing with cURL/Postman

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Create Trek (as Admin)
```bash
curl -X POST http://localhost:5000/api/admin/treks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "trek_name":"Everest Base Camp",
    "location":"Nepal",
    "difficulty":"Hard",
    "duration_days":14,
    "total_slots":20,
    "start_date":"2024-06-01T00:00:00",
    "end_date":"2024-06-14T00:00:00"
  }'
```

### Get Available Treks (as User)
```bash
curl -X GET "http://localhost:5000/api/user/available-treks" \
  -H "Authorization: Bearer <token>"
```

---

## Celery Setup (Background Jobs)

### Prerequisites
- Redis must be installed and running

### Start Redis (if not running)
```bash
# macOS with Homebrew
brew services start redis

# Linux
sudo systemctl start redis

# Windows - Download and run redis-server.exe
```

### Start Celery Worker
```bash
cd backend
celery -A app.tasks worker --loglevel=info
```

### Start Celery Beat (Scheduler)
```bash
cd backend
celery -A app.tasks beat --loglevel=info
```

Scheduled Tasks:
- 📧 Daily reminders at a configured time
- 📊 Monthly activity reports (1st of each month)

---

## Troubleshooting

### Issue: Port 5000 Already in Use
```bash
# Kill the process
lsof -ti:5000 | xargs kill -9

# Or use a different port
python run.py --port 5001
```

### Issue: Redis Connection Error
```bash
# Check if Redis is running
redis-cli ping  # Should return PONG

# Start Redis
redis-server
```

### Issue: Database Not Creating
```bash
# Remove old database
rm backend/trekking_app.db

# Restart the app - it will auto-create
python backend/run.py
```

### Issue: CORS Errors
The backend is already configured with CORS. If issues persist:
- Ensure frontend is on http://localhost:3000
- Ensure backend is on http://localhost:5000
- Clear browser cache

---

## Project Structure Overview

```
├── backend/
│   ├── app/
│   │   ├── models/      # Database schemas
│   │   ├── routes/      # API endpoints
│   │   ├── tasks.py     # Background jobs
│   │   └── extensions.py # Flask setup
│   └── run.py           # Main entry point
│
├── frontend/
│   ├── src/
│   │   ├── views/       # Page components
│   │   ├── store/       # State management
│   │   ├── router/      # Routing
│   │   └── services/    # API client
│   └── vite.config.js   # Build config
│
└── README.md
```

---

## Next Development Steps

1. **Enhance UI Components** - Implement full forms and data tables
2. **Payment Integration** - Add payment simulation
3. **Email Notifications** - Configure SMTP for notifications
4. **PDF Reports** - Generate PDF monthly activity reports
5. **Analytics Dashboard** - Add charts using ChartJS
6. **Validation** - Add form validation (frontend & backend)
7. **Testing** - Create test cases
8. **Deployment** - Docker and production setup

---

## Useful Commands

### Backend
```bash
# Run server
python run.py

# Run with specific environment
FLASK_ENV=production python run.py

# Open Flask shell
flask shell
```

### Frontend
```bash
# Dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Database
```bash
# Access SQLite database
sqlite3 backend/trekking_app.db

# View all tables
.tables

# Exit
.quit
```

---

## Need Help?

Check the main README.md for:
- Detailed API endpoint documentation
- Database schema explanation
- Feature implementation details
- Troubleshooting guide

---

**Happy Trekking!** 🏔️
