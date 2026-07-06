#!/bin/bash
# Queue Management System Setup Script for macOS/Linux

echo ""
echo "========================================="
echo "Queue Management System - Setup Script"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python3 from https://www.python.org/"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/5] Running database migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to run migrations"
    exit 1
fi

echo "[5/5] Setup complete!"
echo ""
echo "========================================="
echo "Next Steps:"
echo "========================================="
echo ""
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Create superuser (admin account):"
echo "   python manage.py createsuperuser"
echo ""
echo "3. Start development server:"
echo "   python manage.py runserver"
echo ""
echo "4. Open browser and go to:"
echo "   http://127.0.0.1:8000/"
echo ""
echo "5. Access admin panel at:"
echo "   http://127.0.0.1:8000/admin/"
echo ""
echo "========================================="
echo ""
