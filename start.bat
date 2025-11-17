@echo off
chcp 65001 >nul
echo ============================================
echo    AIscribe - Medical Transcription System
echo ============================================
echo.
echo Starting AIscribe application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
pip show flask >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

echo.
echo ============================================
echo Starting Flask server...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ============================================
echo.

set PYTHONIOENCODING=utf-8
python app.py

pause

