# VS CODE SETUP AND RUN INSTRUCTIONS

## Step 1: Open Project in VS Code

1. Open VS Code
2. Click "File" → "Open Folder"
3. Navigate to: `C:\Users\Administrator\Desktop\queue\queue_management_system`
4. Click "Select Folder"

## Step 2: Open Integrated Terminal in VS Code

Press: **Ctrl + `** (backtick key)

Or: Click "Terminal" menu → "New Terminal"

## Step 3: Create and Activate Virtual Environment

In the VS Code terminal, run:

```bash
python -m venv venv
```

Then activate it:

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

You should see `(venv)` at the beginning of the terminal prompt.

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Wait for all packages to install (this may take a few minutes).

## Step 5: Run Database Migrations

```bash
python manage.py migrate
```

You should see messages about creating tables in the database.

## Step 6: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

When prompted, enter:
- **Username**: `admin`
- **Email**: `admin@example.com`
- **Password**: Enter a secure password (won't show while typing)
- **Password (again)**: Confirm password

## Step 7: Start Development Server

```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## Step 8: Open in Browser

1. Hold **Ctrl** and click on the URL in the terminal: `http://127.0.0.1:8000/`
2. Or manually open your browser and go to: `http://127.0.0.1:8000/`

## Step 9: Create Admin Profile

To access the admin section (queue management), you need to set your admin user as an admin:

1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with username: `admin` and password: (what you set in Step 6)
3. Click on "User Profiles" in the left menu
4. Find and click on your admin user
5. Check the box "Is admin user"
6. Click "Save" at the bottom

## Step 10: Create Queue Services

1. Go to: `http://127.0.0.1:8000/queue/admin/list/`
2. Click "Create New Queue"
3. Fill in the form:
   - **Service Name**: e.g., "Hospital"
   - **Service Type**: Select from dropdown
   - **Description**: e.g., "General Hospital Queue" (optional)
   - **Estimated Service Time**: e.g., 5 (minutes)
   - Check "Queue is Active"
4. Click "Create Queue"

## Step 11: Test the System

### Create Test User:
1. Click "Register" in the navigation bar
2. Create a new account with different username
3. Login with that account

### Book a Token:
1. Click "Browse Queues"
2. Select a queue
3. Click "Book Token"
4. View your token with QR code
5. See real-time queue position

### Admin Actions:
1. Logout from test account
2. Login as admin
3. Go to "Admin Panel"
4. Click "View Details" on a queue
5. Click "Serve Next" to move queue forward

## Useful Terminal Commands While Development

```bash
# See created migrations
python manage.py showmigrations

# Create new migrations if models changed
python manage.py makemigrations

# Reset database (delete all data)
python manage.py flush

# Open Django shell for testing
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic

# Change server port
python manage.py runserver 8001

# Stop server
Press: Ctrl+C in the terminal
```

## Folder Structure in VS Code

Click the Explorer icon (left sidebar) to see files:

```
queue_management_system/
├── 📄 manage.py
├── 📄 requirements.txt
├── 📁 queue_system/          (Main project settings)
├── 📁 users/                 (User management app)
├── 📁 queue/                 (Queue management app)
├── 📁 booking/               (Token booking app)
├── 📁 templates/             (HTML files)
├── 📁 static/                (CSS and JS files)
│   └── 📁 css/
│       └── 📄 style.css
├── 📁 media/                 (QR code images stored here)
└── 📄 db.sqlite3             (Database file)
```

## File Editing Tips

1. Open any file by pressing **Ctrl+P** and typing filename
2. Common files to edit:
   - `queue_system/settings.py` - Project configuration
   - `static/css/style.css` - Styling
   - `templates/` - HTML files

## Debugging

### If you get an error:

1. **Check Terminal Output**: Error message usually appears in terminal
2. **Check Database**: Run migrations again with `python manage.py migrate`
3. **Restart Server**: Stop (Ctrl+C) and start again
4. **Clear Browser Cache**: Ctrl+Shift+Delete in browser

### Common Issues:

**"ModuleNotFoundError: No module named 'django'"**
- Run: `pip install -r requirements.txt`

**"sqlite3 database is locked"**
- Restart the server

**"Port 8000 already in use"**
- Run: `python manage.py runserver 8001`

**"Template not found"**
- Check file path in `templates/` folder matches the error

## VS Code Extensions Recommended

Open Extensions (Ctrl+Shift+X) and install:
1. **Python** - Microsoft
2. **Django** - Baptiste Darthenay
3. **HTML CSS Support** - ecmel
4. **Prettier** - Code formatter
5. **SQLite** - alexcvzz (to browse database)

## Next Steps

After initial setup:
1. Customize service types in `queue/models.py`
2. Add more templates/pages as needed
3. Configure real email in `queue_system/settings.py`
4. Add SMS notifications
5. Deploy to production

## Keeping Server Running

The server closes when you:
- Close the terminal
- Stop with Ctrl+C
- Close VS Code

To restart: Just run `python manage.py runserver` again

## Admin Accounts

**Superuser (Full Access)**:
- Username: admin
- Used for Django admin and Queue Admin

**Test Users**:
- Create as many as needed via Register button
- Each can book tokens

## URLs Quick Reference

| URL | Purpose |
|-----|---------|
| http://127.0.0.1:8000/ | Home page |
| http://127.0.0.1:8000/users/register/ | User registration |
| http://127.0.0.1:8000/users/login/ | User login |
| http://127.0.0.1:8000/users/dashboard/ | User dashboard |
| http://127.0.0.1:8000/queue/list/ | Browse queues |
| http://127.0.0.1:8000/booking/tokens/ | My tokens |
| http://127.0.0.1:8000/queue/admin/list/ | Admin panel |
| http://127.0.0.1:8000/admin/ | Django admin |

---

**You're all set!** Enjoy using the Queue Management System in VS Code! 🚀
