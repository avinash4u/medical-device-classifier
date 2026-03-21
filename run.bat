@echo off
REM Medical Device Classifier Launcher Script for Windows

echo ==================================
echo Medical Device Classification System
echo MDR 2017 ^& CDSCO Compliant
echo ==================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Checking dependencies...
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt

echo.
echo Starting application...
echo Access the UI at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

REM Run streamlit
streamlit run app.py

pause
