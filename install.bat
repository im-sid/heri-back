@echo off
REM ============================================================
REM Heri-Sci Backend Installation Script (Windows)
REM ============================================================

echo.
echo ============================================================
echo Heri-Sci Backend Installation
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Python detected
python --version
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo Virtual environment created successfully!
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo [4/5] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo [5/5] Installing dependencies...
pip install -r requirements.txt
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ============================================================
    echo IMPORTANT: Please edit .env file and add your API keys!
    echo ============================================================
    echo.
)

REM Create upload directories
if not exist uploads mkdir uploads
if not exist processed mkdir processed

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Edit .env file and add your API keys
echo 2. Run: python app.py
echo 3. Backend will start on http://localhost:5000
echo.
echo To activate virtual environment later:
echo    venv\Scripts\activate
echo.
pause
