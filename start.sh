#!/bin/bash

echo "============================================"
echo "   AIscribe - Medical Transcription System"
echo "============================================"
echo ""
echo "Starting AIscribe application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if dependencies are installed
echo "Checking dependencies..."
if ! pip3 show flask &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

echo ""
echo "============================================"
echo "Starting Flask server..."
echo "Open your browser to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "============================================"
echo ""

python3 app.py



