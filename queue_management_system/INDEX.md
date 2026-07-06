# 📋 INDEX - Complete File & Reference Guide

## 🎯 Start Here

**NEW HERE?** Start with [START_HERE.md](START_HERE.md)

**NEED SETUP HELP?** Choose one:
- Super quick: Run `setup.bat`
- In VS Code: Read [VSCODE_SETUP.md](VSCODE_SETUP.md)
- Detailed: Read [INSTALLATION.md](INSTALLATION.md)

**WANT OVERVIEW?** Read [DELIVERY_SUMMARY.md](DELIVERY_SUMMARY.md)

---

## 📚 Documentation Files (Read These)

| File | Size | Purpose |
|------|------|---------|
| [START_HERE.md](START_HERE.md) | 5 min read | Quick intro & setup |
| [README.md](README.md) | 10 min read | Full documentation |
| [VSCODE_SETUP.md](VSCODE_SETUP.md) | 10 min read | VS Code step-by-step |
| [INSTALLATION.md](INSTALLATION.md) | 15 min read | Detailed installation |
| [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | 15 min read | Architecture & design |
| [FILE_LISTING.md](FILE_LISTING.md) | 10 min read | File structure |
| [DELIVERY_SUMMARY.md](DELIVERY_SUMMARY.md) | 5 min read | What's included |
| [QUICKSTART.txt](QUICKSTART.txt) | 2 min read | Quick reference |

**Total Documentation:** ~2,600 lines

---

## ⚙️ Setup Files (Run These)

| File | OS | Purpose |
|------|----|----|
| [setup.bat](setup.bat) | Windows | Automatic setup |
| [setup.sh](setup.sh) | Linux/Mac | Automatic setup |

---

## 🐍 Django Project Files (Don't Modify Yet)

```
queue_system/
├── __init__.py
├── settings.py          [All project configuration]
├── urls.py              [Main URL routing]
└── wsgi.py              [WSGI application]

manage.py               [Main Django command file]
requirements.txt        [Python packages to install]
.gitignore              [Git ignore rules]
db.sqlite3              [Database - auto-created]
```

---

## 👥 Users App (User Management)

```
users/
├── __init__.py
├── apps.py
├── models.py            [UserProfile model]
├── views.py             [Register, login, dashboard]
├── forms.py             [Registration & profile forms]
├── urls.py              [User URLs]
├── admin.py             [Admin configuration]
└── tests.py             [Unit tests]

migrations/             [Database migrations - auto-created]
```

**Models:** UserProfile

**Views:** Register, Login, Logout, Dashboard, Profile

**URLs:** /users/register/, /users/login/, /users/logout/, /users/dashboard/, /users/profile/

---

## 🏢 Queue App (Queue Management)

```
queue/
├── __init__.py
├── apps.py
├── models.py            [QueueService model]
├── views.py             [Queue operations - admin & user]
├── forms.py             [Queue creation form]
├── urls.py              [Queue URLs]
├── admin.py             [Admin configuration]
└── tests.py             [Unit tests]

migrations/             [Database migrations - auto-created]
```

**Models:** QueueService

**Views:** Queue list, detail, admin list, create, update, detail, serve-next

**URLs:** /queue/list/, /queue/<id>/, /queue/admin/list/, /queue/admin/create/, /queue/admin/<id>/update/, /queue/admin/<id>/detail/, /queue/admin/<id>/serve-next/

---

## 🎫 Booking App (Token Management)

```
booking/
├── __init__.py
├── apps.py
├── models.py            [Token, Booking, Notification models]
├── views.py             [Token booking, QR generation,notifications]
├── forms.py             [Booking forms]
├── urls.py              [Booking URLs]
├── admin.py             [Admin configuration]
├── tests.py             [Unit tests]
├── templatetags/
│   ├── __init__.py
│   ├── booking_tags.py  [Custom template filters]
│   ├── queue_tags.py    [Queue filtering]
│   └── user_tags.py     [User profile filters]
└── templatetags.py      [Can be deleted - older version]

migrations/             [Database migrations - auto-created]
```

**Models:** Token, Booking, Notification

**Views:** Book token, view token, cancel, token list, API endpoints

**URLs:** /booking/book/<queue_id>/, /booking/token/<id>/, /booking/token/<id>/cancel/, /booking/tokens/, /booking/api/token-position/<id>/

---

## 🎨 Templates (HTML Files)

```
templates/
├── base.html                        [Main layout with navbar]
├── home.html                        [Home page]
├── users/
│   ├── register.html                [Registration page]
│   ├── login.html                   [Login page]
│   ├── dashboard.html               [User dashboard]
│   └── profile.html                 [Profile edit]
├── queue/
│   ├── queue_list.html              [Browse queues]
│   ├── queue_detail.html            [Queue detail]
│   ├── admin_queue_list.html        [Admin queue list]
│   ├── admin_queue_form.html        [Create/edit queue]
│   └── admin_queue_detail.html      [Queue management]
└── booking/
    ├── book_token.html              [Book token form]
    ├── token_detail.html            [Token with QR]
    └── token_list.html              [Token history]
```

**Total:** 13 HTML files

---

## 🎨 Static Files (Styling)

```
static/
├── css/
│   └── style.css                    [All styling - 870+ lines]
└── js/
    └─ (JavaScript in templates)
```

---

## 📁 Media Folder (Auto-Created)

```
media/
└── qr_codes/                        [Generated QR code images]
```

Auto-generated when tokens are booked.

---

## 🔧 Configuration Reference

### Database (settings.py)
- Type: SQLite3
- File: db.sqlite3
- No external setup needed

### Installed Apps
- users
- queue
- booking
- django.contrib.admin
- django.contrib.auth
- django.contrib.contenttypes
- django.contrib.sessions
- django.contrib.messages
- django.contrib.staticfiles
- crispy_forms
- crispy_bootstrap5

### Authentication
- Backend: Django default (PBKDF2)
- Login URL: /users/login/
- Redirect: /users/dashboard/

---

## 🌐 URLs Quick Reference

### Public Pages (No Login)
```
/                               [Home page]
/users/register/                [Registration]
/users/login/                   [Login]
```

### User Pages (Login Required)
```
/users/dashboard/               [Dashboard]
/users/profile/                 [Profile]
/users/logout/                  [Logout]
/queue/list/                    [Browse queues]
/queue/<id>/                    [Queue detail]
/booking/book/<queue_id>/       [Book token]
/booking/token/<id>/            [Token detail]
/booking/token/<id>/cancel/     [Cancel token]
/booking/tokens/                [My tokens]
```

### Admin Pages (Admin Only)
```
/queue/admin/list/              [Admin dashboard]
/queue/admin/create/            [Create queue]
/queue/admin/<id>/update/       [Edit queue]
/queue/admin/<id>/detail/       [Queue detail]
/queue/admin/<id>/serve-next/   [Serve next]
```

### API Endpoints (JSON)
```
/queue/api/status/<id>/         [Queue status]
/booking/api/token-position/<id>/ [Token position]
```

### Django Admin
```
/admin/                         [Django admin panel]
```

---

## 📊 Database Models

### UserProfile
- user (OneToOne → User)
- phone_number (CharField)
- is_admin_user (BooleanField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### QueueService
- admin (ForeignKey → User)
- service_name (CharField)
- service_type (CharField with choices)
- description (TextField)
- estimated_service_time (IntegerField)
- is_active (BooleanField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### Token
- queue (ForeignKey → QueueService)
- user (ForeignKey → User)
- token_number (IntegerField)
- unique_id (CharField - UUID)
- status (CharField with choices)
- qr_code (ImageField)
- notification_sent (BooleanField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### Booking
- user (ForeignKey → User)
- queue (ForeignKey → QueueService)
- token (OneToOne → Token, nullable)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### Notification
- token (ForeignKey → Token)
- notification_type (CharField with choices)
- message (TextField)
- is_sent (BooleanField)
- created_at (DateTimeField)

---

## 📦 Python Packages

```
Django==4.2.0                   [Web framework]
django-crispy-forms==2.1        [Form styling]
crispy-bootstrap5==0.7          [Bootstrap integration]
Pillow==10.0.0                  [Image processing]
qrcode==7.4.2                   [QR code generation]
python-dotenv==1.0.0            [Environment variables]
```

All specified in `requirements.txt`

---

## 🧪 Features By File

### User Registration
- Location: `users/views.py` → `register()`
- Form: `users/forms.py` → `UserRegistrationForm`
- Template: `users/register.html`

### Token Booking
- Location: `booking/views.py` → `book_token()`
- Model: `booking/models.py` → `Token`
- Template: `booking/book_token.html`
- QR Generation: Auto in `Token.save()`

### Queue Management
- Location: `queue/views.py` → `admin_*` functions
- Model: `queue/models.py` → `QueueService`
- Template: `queue/admin_*.html`

### Notifications
- Location: `booking/views.py` → `send_notification_if_needed()`
- Model: `booking/models.py` → `Notification`
- Trigger: When 3 people or fewer ahead

---

## 🚀 Quick Commands

```bash
# Setup (Windows)
double-click setup.bat

# Setup (Linux/Mac)
bash setup.sh

# Activate venv
venv\Scripts\activate (Windows)
source venv/bin/activate (Linux/Mac)

# Run server
python manage.py runserver

# Create admin
python manage.py createsuperuser

# Database
python manage.py migrate
python manage.py makemigrations

# Reset
python manage.py flush
```

---

## 📞 Help Files

| When You... | Read |
|-------------|------|
| Don't know where to start | [START_HERE.md](START_HERE.md) |
| Are setting up | [VSCODE_SETUP.md](VSCODE_SETUP.md) |
| Have errors | [INSTALLATION.md](INSTALLATION.md) |
| Want full details | [README.md](README.md) |
| Want architecture | [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) |
| Need file reference | [FILE_LISTING.md](FILE_LISTING.md) |
| Quick overview | [DELIVERY_SUMMARY.md](DELIVERY_SUMMARY.md) |

---

## ✅ Checklist After Setup

- [ ] Run `setup.bat` or follow [VSCODE_SETUP.md](VSCODE_SETUP.md)
- [ ] Server running at http://127.0.0.1:8000/
- [ ] Created superuser account
- [ ] Set admin user in Django admin
- [ ] Created queue service
- [ ] Booked test token
- [ ] Can see QR code
- [ ] Admin panel working
- [ ] No errors in terminal

---

## 📈 Project Statistics

| Metric | Value |
|--------|-------|
| Total Files | 34 |
| Code Files | 24 |
| Documentation | 8 |
| Setup Scripts | 2 |
| Total Lines | ~2,700 |
| HTML Lines | ~900 |
| CSS Lines | ~870 |
| Python Lines | ~1,500 |
| Installation Time | 5-15 min |
| First Token Time | <5 min |

---

## 🎓 Learning Path

1. **Read:** [START_HERE.md](START_HERE.md) (5 min)
2. **Setup:** Follow setup guide (10-15 min)
3. **Explore:** Browse code & templates (20 min)
4. **Test:** Book tokens, use admin (10 min)
5. **Customize:** Edit CSS, add features (your time)

Total: ~1 hour to fully understand

---

## 🔐 Security Features

✓ All user passwords hashed
✓ CSRF protection enabled
✓ SQL injection prevention
✓ XSS protection
✓ Login decorators on protected views
✓ Admin role verification
✓ Session management
✓ Input validation

---

## 🌍 Browser Testing

Tested on:
✓ Chrome
✓ Firefox
✓ Safari
✓ Edge
✓ Mobile browsers

---

## 📱 Responsive Design

✓ Mobile friendly (320px+)
✓ Tablet friendly (768px+)
✓ Desktop optimized (1200px+)
✓ Bootstrap 5 responsive grid

---

## 🎉 Success Indicators

When you see:
✓ Home page with navbar
✓ Can register/login
✓ Can browse queues
✓ Can book and get QR code
✓ Real-time position updates
✓ Admin panel works
✓ No errors in terminal

...the system is working perfectly!

---

## 📧 Contact Points in Code

All email logic in: `booking/views.py` → `send_notification_if_needed()`

Can be configured for:
- Gmail
- AWS SES
- SendGrid
- Any SMTP server

---

## 🔄 Next Steps

1. **Immediate:** Get running (1 hour)
2. **Short-term:** Customize styling (2 hours)
3. **Medium-term:** Add SMS notifications (4 hours)
4. **Long-term:** Deploy to production (1 day)

---

## 📞 Common Questions

**Q: How to change colors?**
A: Edit `static/css/style.css`

**Q: How to add service types?**
A: Edit `queue/models.py` → `SERVICE_CHOICES`

**Q: How to configure email?**
A: Edit `queue_system/settings.py` → `EMAIL_*` settings

**Q: How to make user admin?**
A: Go to Django admin, edit UserProfile, check "Is admin user"

**Q: How to reset database?**
A: Run: `python manage.py flush`

---

## 🚀 Ready to Start?

→ [START_HERE.md](START_HERE.md)

Or just run: `setup.bat`

---

**Welcome to Queue Management System!** 🎉

Everything you need is included. Happy coding! 😊
