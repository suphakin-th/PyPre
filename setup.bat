@echo off
echo ================================================
echo    📊 DataBoard - Setup Script
echo ================================================
echo.

REM Check Python
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Error: Python not found! Please install Python 3.7 or higher
    pause
    exit /b 1
)
echo.

REM Create virtual environment
set /p create_venv="Create virtual environment? (recommended) [y/N]: "
if /i "%create_venv%"=="y" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Virtual environment activated
    echo.
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Create directories
echo Creating data directories...
if not exist "data\uploads" mkdir data\uploads
if not exist "data\datasets" mkdir data\datasets
if not exist "data\dashboards" mkdir data\dashboards
if not exist "static" mkdir static
echo Directories created
echo.

echo ================================================
echo    ✅ Setup Complete!
echo ================================================
echo.
echo To start the server:
echo   python app.py
echo.
echo Then open your browser to:
echo   http://localhost:5000
echo.
echo Default credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo ================================================
pause
