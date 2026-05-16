from celery import shared_task
from app.extensions import db, celery_app
from app.models import Booking, Trek, User
import csv
from io import StringIO
from datetime import datetime, timedelta

@shared_task
def export_user_booking_csv(user_id):
    """Export user booking history to CSV"""
    user = User.query.get(user_id)
    if not user:
        return {'status': 'error', 'message': 'User not found'}
    
    bookings = Booking.query.filter_by(user_id=user_id).all()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Booking ID', 'Trek Name', 'Location', 'Difficulty', 'Start Date', 'End Date', 'Booking Status', 'Payment Status'])
    
    # Data rows
    for booking in bookings:
        writer.writerow([
            booking.id,
            booking.trek.trek_name,
            booking.trek.location,
            booking.trek.difficulty,
            booking.trek.start_date,
            booking.trek.end_date,
            booking.booking_status,
            booking.payment_status
        ])
    
    csv_content = output.getvalue()
    
    # Save or send file (for now, just return success)
    return {
        'status': 'completed',
        'user_id': user_id,
        'total_bookings': len(bookings),
        'timestamp': datetime.utcnow().isoformat()
    }

@shared_task
def send_daily_trek_reminders():
    """Send daily reminders to users about upcoming treks"""
    tomorrow = datetime.utcnow() + timedelta(days=1)
    start_of_day = tomorrow.replace(hour=0, minute=0, second=0)
    end_of_day = tomorrow.replace(hour=23, minute=59, second=59)
    
    # Find treks starting tomorrow
    upcoming_treks = Trek.query.filter(
        Trek.start_date >= start_of_day,
        Trek.start_date <= end_of_day,
        Trek.status.in_(['Open', 'Approved'])
    ).all()
    
    reminders_sent = 0
    
    for trek in upcoming_treks:
        # Get all users booked for this trek
        bookings = Booking.query.filter_by(trek_id=trek.id, booking_status='Booked').all()
        
        for booking in bookings:
            user = booking.user
            # Send email/notification to user
            # send_reminder_email(user.email, trek)
            reminders_sent += 1
    
    return {
        'status': 'completed',
        'reminders_sent': reminders_sent,
        'treks_with_reminders': len(upcoming_treks),
        'timestamp': datetime.utcnow().isoformat()
    }

@shared_task
def generate_monthly_activity_report():
    """Generate monthly activity report for admin"""
    # Get admin user
    admin = User.query.filter_by(user_type='admin').first()
    if not admin:
        return {'status': 'error', 'message': 'Admin not found'}
    
    # Calculate stats for current month
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    if now.month == 12:
        month_end = month_start.replace(year=now.year + 1, month=1) - timedelta(days=1)
    else:
        month_end = month_start.replace(month=now.month + 1) - timedelta(days=1)
    
    # Get stats
    completed_treks = Trek.query.filter(
        Trek.status == 'Completed',
        Trek.end_date >= month_start,
        Trek.end_date <= month_end
    ).count()
    
    total_bookings = Booking.query.filter(
        Booking.created_at >= month_start,
        Booking.created_at <= month_end
    ).count()
    
    completed_bookings = Booking.query.filter(
        Booking.booking_status == 'Completed',
        Booking.updated_at >= month_start,
        Booking.updated_at <= month_end
    ).count()
    
    total_users = User.query.filter_by(user_type='user').count()
    
    # Generate HTML report
    html_content = f"""
    <html>
    <head><title>Monthly Activity Report</title></head>
    <body>
        <h1>Trekking Management System - Monthly Report</h1>
        <p>Month: {now.strftime('%B %Y')}</p>
        <h2>Statistics</h2>
        <ul>
            <li>Completed Treks: {completed_treks}</li>
            <li>Total Bookings: {total_bookings}</li>
            <li>Completed Bookings: {completed_bookings}</li>
            <li>Total Users: {total_users}</li>
        </ul>
        <p>Report Generated: {datetime.utcnow().isoformat()}</p>
    </body>
    </html>
    """
    
    # Send email to admin
    # send_monthly_report_email(admin.email, html_content)
    
    return {
        'status': 'completed',
        'admin_id': admin.id,
        'month': now.strftime('%B %Y'),
        'stats': {
            'completed_treks': completed_treks,
            'total_bookings': total_bookings,
            'completed_bookings': completed_bookings,
            'total_users': total_users
        },
        'timestamp': datetime.utcnow().isoformat()
    }
