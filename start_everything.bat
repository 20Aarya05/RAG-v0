@echo off
title RAG System Startup
color 0A

echo.
echo ========================================
echo 🚀 RAG Document Processing System
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo ❌ Error: backend folder not found!
    echo 💡 Please run this script from the RAG project root directory
    echo    Current directory: %CD%
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ❌ Error: frontend folder not found!
    echo 💡 Please run this script from the RAG project root directory
    pause
    exit /b 1
)

echo ✅ Project structure verified
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found! Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js found: 
node --version
echo.

REM Check if virtual environment exists
if not exist "backend\venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found in backend\venv
    echo 💡 Please run the backend setup first
    pause
    exit /b 1
)

echo ✅ Virtual environment found
echo.

REM Install frontend dependencies if needed
if not exist "frontend\node_modules" (
    echo 📦 Installing frontend dependencies...
    cd frontend
    npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install frontend dependencies
        cd ..
        pause
        exit /b 1
    )
    cd ..
    echo ✅ Frontend dependencies installed
) else (
    echo ✅ Frontend dependencies already installed
)

echo.
echo 🔄 Starting services...
echo.

REM Start backend API server
echo 📡 Starting Backend API Server...
start "RAG Backend API" /D "%CD%\backend" cmd /k "venv\Scripts\activate.bat && echo ✅ Virtual environment activated && echo 🚀 Starting API server... && python api_server.py"

REM Wait for backend to start
echo ⏳ Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Start frontend development server
echo 🌐 Starting Frontend Development Server...
start "RAG Frontend" /D "%CD%\frontend" cmd /k "echo 🚀 Starting frontend... && npm run dev"

REM Wait a moment
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo 🎉 RAG System Started Successfully!
echo ========================================
echo.
echo 📡 Backend API:     http://localhost:8000
echo 🌐 Frontend App:    http://localhost:3000  
echo 📚 API Docs:        http://localhost:8000/docs
echo.
echo 💡 Two terminal windows have opened:
echo    1. Backend API Server (Python)
echo    2. Frontend Dev Server (Node.js)
echo.
echo ⚠️  Keep both terminals open while using the system
echo.

REM Ask if user wants to open browser
set /p openBrowser="🌐 Open the application in your browser? (y/N): "
if /i "%openBrowser%"=="y" (
    echo 🔄 Opening browser...
    timeout /t 2 /nobreak >nul
    start http://localhost:3000
)

echo.
echo 📋 Quick Usage Guide:
echo    • Upload Tab: Drag & drop files to upload
echo    • Files Tab: View and manage documents  
echo    • Status Tab: Monitor processing progress
echo    • Config Tab: View embedding settings
echo.
echo 🛑 To stop the system:
echo    • Close both terminal windows, or
echo    • Press Ctrl+C in each terminal
echo.
echo 🆘 If you encounter issues:
echo    • Check both terminal windows for errors
echo    • Run: python test_setup.py
echo    • See STARTUP_GUIDE.md for detailed help
echo.

pause