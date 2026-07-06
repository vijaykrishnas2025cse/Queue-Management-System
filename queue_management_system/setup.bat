@echo off
REM Queue Management System Setup Script for Windows

echo.
echo =========================================
echo Queue Management System - Setup Script
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Running database migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo [5/5] Setup complete!
echo.
echo =========================================
echo Next Steps:
echo =========================================
echo.
echo 1. Activate virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Create superuser (admin account):
echo    python manage.py createsuperuser
echo.
echo 3. Start development server:
echo    python manage.py runserver
echo.
echo 4. Open browser and go to:
echo    http://127.0.0.1:8000/
echo.
echo 5. Access admin panel at:
echo    http://127.0.0.1:8000/admin/
echo.
echo =========================================
echo.
pause
