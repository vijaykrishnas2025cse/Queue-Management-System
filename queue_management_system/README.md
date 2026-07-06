# Django Queue Management System

A complete full-stack Queue Management System built with Python Django, HTML, CSS, and Bootstrap.

## Features

### User Features
- ✅ User Registration and Login with secure authentication
- ✅ Book slots (tokens) in queues for different services
- ✅ Unique QR code generation for each token
- ✅ Real-time queue position tracking
- ✅ Email notifications when 3 people or fewer are ahead
- ✅ Token history and booking management
- ✅ User profile management

### Admin Features
- ✅ Create and manage multiple queue services
- ✅ View all users and tokens in each queue
- ✅ Move queue forward (serve next user)
- ✅ Verify/scan QR codes
- ✅ Queue settings and management
- ✅ Real-time queue monitoring dashboard

### Technical Features
- ✅ Django ORM with proper database models
- ✅ User authentication system
- ✅ QR code generation (qrcode library)
- ✅ Bootstrap 5 responsive UI
- ✅ Real-time status updates (auto-refresh)
- ✅ Email notification system
- ✅ Admin panel for queue management
- ✅ JSON API endpoints for real-time data

## Project Structure

```
queue_management_system/
├── manage.py
├── requirements.txt
├── queue_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── queue/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── booking/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── users/
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   └── profile.html
│   ├── booking/
│   │   ├── book_token.html
│   │   ├── token_detail.html
│   │   └── token_list.html
│   └── queue/
│       ├── queue_list.html
│       ├── queue_detail.html
│       ├── admin_queue_list.html
│       ├── admin_queue_form.html
│       └── admin_queue_detail.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
├── media/
│   └── qr_codes/
└── db.sqlite3
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Step 1: Clone or Download the Project

```bash
# Navigate to the project directory
cd queue_management_system
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Database

Run migrations to set up the database:

```bash
python manage.py migrate
```

### Step 5: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

When prompted, enter:
- Username: `admin`
- Email: `admin@example.com`
- Password: (choose a secure password)

### Step 6: Create Initial Queue Services (Optional)

You can create queue services through the Django admin panel or use the management command if available.

### Step 7: Run Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## Usage Guide

### For Users

1. **Register**: Click "Register" and create a new account
2. **Login**: Log in with your credentials
3. **Browse Queues**: Go to "Browse Queues" to see available services
4. **Book Token**: Select a queue and click "Book Token"
5. **View Token**: Your token details, QR code, and queue position
6. **Get Notifications**: When 3 or fewer people are ahead, you'll get an email
7. **Cancel Token**: You can cancel your token if you haven't been served yet

### For Admins

1. **Login**: Use superuser credentials
2. **Admin Panel**: Navigate to "Admin Panel" (only visible to admin users)
3. **Create Queue**: Click "Create New Queue" to add a new service
4. **Manage Queues**: View all your queues and their status
5. **Serve Next**: Click "Serve Next" to move the queue forward
6. **View Details**: Check token details and user information
7. **Edit Queue**: Update queue settings (name, service time, status)

### Marking User as Admin

To make a user an admin, modify their profile through Django admin:

1. Go to `/admin/` (e.g., http://127.0.0.1:8000/admin/)
2. Login with superuser credentials
3. Go to "User Profiles"
4. Select a user and check "Is admin user"
5. Save

## Database Models

### UserProfile
- Extends Django's User model
- Stores phone number and admin status
- One-to-one relationship with User

### QueueService
- Represents a queue for a specific service
- Stores service name, type, description
- Tracks estimated service time
- Admin can create and manage

### Token
- Represents a booking slot
- Unique ID and token number
- Stores QR code image
- Tracks status (waiting, ready, serving, completed, cancelled)
- Automatically generates QR code on creation

### Booking
- Records of user bookings
- Links to User, QueueService, and Token
- Maintains booking history

### Notification
- Stores notification records sent to users
- Tracks notification type (email, SMS)
- Records whether notification was sent

## API Endpoints

### Queue Status
- `GET /queue/api/status/<queue_id>/` - Get real-time queue status

### Token Position
- `GET /booking/api/token-position/<token_id>/` - Get real-time token position

Both endpoints return JSON data for frontend updates.

## Email Configuration

Currently configured for console output (development). To use real email:

Edit `queue_system/settings.py`:

```python
# For Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

## Customization

### Change Service Types
Edit `queue/models.py`, SERVICE_CHOICES in QueueService model

### Change Colors
Edit `static/css/style.css`, modify CSS variables

### Adjust Auto-Refresh Rate
Edit template JavaScript in `templates/booking/token_detail.html` and `templates/queue/queue_detail.html`

### Change Notification Trigger
Edit `booking/views.py`, modify the `send_notification_if_needed()` function

## Troubleshooting

### Migrations Issue
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Database Issues
```bash
# Remove existing database
rm db.sqlite3
# Recreate migrations
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Permission Denied (Admin Features)
Make sure the user profile has "Is admin user" checkbox enabled in Django admin panel at `/admin/users/userprofile/`

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Security Notes

- Change `SECRET_KEY` in `settings.py` for production
- Set `DEBUG = False` for production
- Use HTTPS in production
- Implement CORS for API if needed
- Add CSRF protection (already enabled)
- Use environment variables for sensitive data

## Performance Optimization

- Add database indexing for frequently queried fields
- Implement caching with Redis
- Use Celery for background tasks (notifications)
- Compress static files for production
- Implement pagination for large token lists

## Future Enhancements

- SMS notifications via Twilio or AWS SNS
- Real-time WebSocket updates (Django Channels)
- Mobile app (React Native or Flutter)
- Analytics dashboard
- Queue analytics and reporting
- Advanced scheduling system
- Integration with calendaring systems
- Bill payments integration
- Multi-language support

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django documentation
3. Check template error messages
4. Review console/terminal output
5. Check Django admin panel for data

## License

This project is open source and available for educational and commercial use.

## Author

Built as a complete Django project tutorial and application example.

---

**Enjoy using the Queue Management System!** 🎉

For any improvements or suggestions, feel free to extend and customize the project.
