#!/bin/bash

# Medical Device Classifier Launcher Script

echo "=================================="
echo "Medical Device Classification System"
echo "MDR 2017 & CDSCO Compliant"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Checking dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "Starting application..."
echo "Access the UI at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Run streamlit
streamlit run app.py
