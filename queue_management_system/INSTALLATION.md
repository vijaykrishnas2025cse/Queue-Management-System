# INSTALLATION GUIDE - Queue Management System

## Complete Step-by-Step Setup Instructions

### System Requirements
- Windows 10/11 with Administrator access
- Python 3.8 or higher
- pip (comes with Python)
- Internet connection to download packages
- ~500 MB free disk space

### Project Location
```
C:\Users\Administrator\Desktop\queue\queue_management_system
```

---

## METHOD 1: Automatic Setup (Recommended)

### For Windows Users:

1. Open File Explorer
2. Navigate to: `C:\Users\Administrator\Desktop\queue\queue_management_system`
3. Double-click `setup.bat`
4. Wait for the script to complete
5. When finished, a Command Prompt will show next steps
6. Follow the instructions in that window

---

## METHOD 2: Manual Setup Using VS Code (Detailed)

### Step 1: Open Project in VS Code

1. **Open VS Code** on your computer
2. Click **File** → **Open Folder**
3. Navigate to: `C:\Users\Administrator\Desktop\queue\queue_management_system`
4. Click **Select Folder**
5. Wait for VS Code to load the folder

### Step 2: Open Terminal in VS Code

**Option A (Fastest):**
- Press: `Ctrl + `` (the backtick key, usually top-left of keyboard)

**Option B:**
- Click menu: **Terminal** → **New Terminal**
- Click menu: **View** → **Terminal**

You should see a command prompt window at the bottom of VS Code.

### Step 3: Create Python Virtual Environment

Copy and paste this command into the terminal:

```bash
python -m venv venv
```

Press **Enter** and wait. It will create a folder called `venv`.

### Step 4: Activate Virtual Environment

**For Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**For Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**For macOS/Linux:**
```bash
source venv/bin/activate
```

After running this, you should see `(venv)` at the start of terminal lines.

### Step 5: Install All Required Packages

Copy and paste:

```bash
pip install -r requirements.txt
```

Press **Enter**. This will download and install:
- Django 4.2.0
- QR code library
- Bootstrap integration
- Database tools
- Other dependencies

**This may take 5-10 minutes.** Wait for it to complete. You'll see:
```
Successfully installed Django ...
```

### Step 6: Create Database and Run Migrations

Copy and paste:

```bash
python manage.py migrate
```

Press **Enter**. This creates the database tables. You'll see many lines starting with "OK" or "Operations to perform".

### Step 7: Create Admin Account

Copy and paste:

```bash
python manage.py createsuperuser
```

You'll be prompted to enter:

```
Username: admin
Email address: admin@example.com
Password: (type password, won't show)
Password (again): (retype password)
Superuser created successfully.
```

**Important: Remember these credentials!**

### Step 8: Start Development Server

Copy and paste:

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 9: Open in Web Browser

1. **Option A (Click):** Hold Ctrl and click the URL in terminal
2. **Option B (Manual):** Copy the URL and paste in your browser
3. **Option C (Type):** Open browser and go to: `http://127.0.0.1:8000/`

You should see the Queue Management System home page!

---

## First-Time Setup Configuration

### Step 1: Set Admin User as Queue Admin

1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with username: `admin` and your password
3. In left menu, click **User Profiles**
4. Click on the `admin` user profile
5. **Check the box** next to "Is admin user"
6. Scroll down and click **SAVE**
7. You're now an admin!

### Step 2: Create a Sample Queue Service

1. Go back to: `http://127.0.0.1:8000/queue/admin/list/`
2. Click blue button: **Create New Queue**
3. Fill in the form:

| Field | Example Value |
|-------|---|
| Service Name | Hospital |
| Service Type | Hospital (select from dropdown) |
| Description | General Hospital OPD Queue | (optional)
| Est. Service Time | 5 (in minutes) |
| Queue is Active | ☑ (check this) |

4. Click **Create Queue**

### Step 3: Create a Test User Account

1. Click **Register** in top navigation
2. Fill in:
   - Username: testuser
   - Email: test@example.com
   - Phone Number: 9876543210 (optional)
   - Password: testpass123
   - Confirm Password: testpass123
3. Click **Register**
4. Click **Login** and login with testuser

### Step 4: Test Token Booking

1. Click **Browse Queues** in navigation
2. You should see "Hospital" queue with 5 min estimate
3. Click **Book Token**
4. Click **Book Token Now**
5. You'll get a unique token with QR code!

### Step 5: Test Admin Features

1. Logout (click username dropdown → Logout)
2. Login as admin
3. Click **Admin Panel** (only visible to admins)
4. Click **View Details** on Hospital queue
5. Click **Serve Next** to move queue forward
6. Check status changes

---

## Folder Structure Explained

```
queue_management_system/
│
├── manage.py
│   └─ Main file to run commands
│
├── requirements.txt
│   └─ List of all packages needed
│
├── db.sqlite3
│   └─ Database (created after migration)
│
├── queue_system/
│   └─ Main project configuration folder
│
├── users/
│   ├─ models.py: User database structure
│   ├─ views.py: Handle login/register
│   └─ urls.py: User URLs (/users/login, /users/register)
│
├── queue/
│   ├─ models.py: Queue database structure
│   ├─ views.py: Handle queue operations
│   └─ urls.py: Queue URLs (/queue/list, /queue/admin/)
│
├── booking/
│   ├─ models.py: Token/Booking structure
│   ├─ views.py: Handle token booking
│   └─ urls.py: Booking URLs (/booking/book, /booking/tokens/)
│
├── templates/
│   ├─ base.html: Main template with navbar
│   ├─ home.html: Home page
│   ├─ users/: User templates
│   ├─ queue/: Queue templates
│   └─ booking/: Booking templates
│
├── static/
│   ├─ css/
│   │  └─ style.css: All styling
│   └─ js/: JavaScript files (if added)
│
└── media/
   └─ qr_codes/: Generated QR code images
```

---

## All Important URLs

### User Pages
- **Home:** `http://127.0.0.1:8000/`
- **Register:** `http://127.0.0.1:8000/users/register/`
- **Login:** `http://127.0.0.1:8000/users/login/`
- **Dashboard:** `http://127.0.0.1:8000/users/dashboard/`
- **Profile:** `http://127.0.0.1:8000/users/profile/`

### Queue Pages
- **Browse Queues:** `http://127.0.0.1:8000/queue/list/`
- **Queue Detail:** `http://127.0.0.1:8000/queue/1/` (replace 1 with queue ID)

### Booking Pages
- **My Tokens:** `http://127.0.0.1:8000/booking/tokens/`
- **Token Detail:** `http://127.0.0.1:8000/booking/token/1/` (replace 1 with token ID)

### Admin Pages
- **Admin Panel:** `http://127.0.0.1:8000/queue/admin/list/`
- **Queue Management:** `http://127.0.0.1:8000/queue/admin/list/`

### Django Admin
- **Django Admin:** `http://127.0.0.1:8000/admin/`

---

## Terminal Commands Reference

### Basic Commands
```bash
# Start server (main command you'll use)
python manage.py runserver

# Start on different port
python manage.py runserver 8001

# Create database tables
python manage.py migrate

# Create new migrations
python manage.py makemigrations

# Reset database (WARNING: deletes all data!)
python manage.py flush

# Create superuser
python manage.py createsuperuser
```

### When You're Done
To stop the server: Press `Ctrl + C` in the terminal

---

## Running Again (After First Setup)

If you close VS Code and want to run the project again:

1. Open VS Code
2. Open the project folder
3. Open Terminal (Ctrl + `)
4. Activate venv: `venv\Scripts\activate`
5. Run: `python manage.py runserver`
6. Open: `http://127.0.0.1:8000/`

That's it! No need to reinstall or reconfigure.

---

## Common Problems & Solutions

### Problem: "pip: command not found"
**Solution:** Python isn't in PATH. Reinstall Python with "Add Python to PATH" checked.

### Problem: "No module named 'django'"
**Solution:** Run: `pip install -r requirements.txt` again

### Problem: "port 8000 already in use"
**Solution:** Run: `python manage.py runserver 8001` (or change 8001 to any free port)

### Problem: Database locked error
**Solution:** Stop server (Ctrl+C) and restart

### Problem: Static files not showing (no CSS)
**Solution:** Run: `python manage.py collectstatic`

### Problem: Can't login to admin
**Solution:** 
1. Check username/password
2. Make sure user has "Is admin user" checked
3. Verify in django admin at `/admin/`

### Problem: QR code not showing
**Solution:** 
1. Make sure media folder exists
2. Restart server
3. Check file permissions

### Problem: Migrations failing
**Solution:** 
```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

---

## After Setup: Customization

### Add More Service Types
Edit: `queue/models.py` → Find `SERVICE_CHOICES` → Add new types

### Change Colors/Styling
Edit: `static/css/style.css` → Modify colors

### Add Notification Email
Edit: `queue_system/settings.py` → Configure EMAIL settings

### Change Estimated Service Time
When creating a queue, set different times per service

---

## Production Deployment

Before publishing online:

1. **Change SECRET_KEY** in `queue_system/settings.py`
2. **Set DEBUG = False** in settings
3. **Get SSL certificate** (HTTPS)
4. **Use real database** (PostgreSQL)
5. **Configure email** properly
6. **Add domain name**
7. **Use production server** (Gunicorn, etc.)
8. **Collect static files:** `python manage.py collectstatic`

---

## System Specs Used

- **Python:** 3.8+
- **Django:** 4.2.0
- **Database:** SQLite3 (built-in)
- **Frontend:** Bootstrap 5, HTML5, CSS3
- **QR Code:** qrcode 7.4.2
- **Framework:** Pure Django (no SPA)

---

## Success Indicators

✅ You see home page after opening URL
✅ You can register new user
✅ You can  login/logout
✅ You can browse queues
✅ You can book tokens with QR code
✅ You can see admin panel
✅ You can serve next in queue
✅ No errors in terminal

---

**Setup Complete! Enjoy Your Queue Management System! 🎉**

For more details, see README.md and VSCODE_SETUP.md
