@echo off
echo 🚀 Starting RAG System - Frontend + Backend
echo ==========================================

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found! Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo ✅ Node.js and Python found

REM Install frontend dependencies if needed
if not exist "frontend\node_modules" (
    echo 📦 Installing frontend dependencies...
    cd frontend
    npm install
    cd ..
)

REM Start backend API server
echo 🔄 Starting backend API server...
start "RAG Backend API" cmd /k "cd backend && .\venv\Scripts\activate && python api_server.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend development server
echo 🔄 Starting frontend development server...
start "RAG Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo 🎉 System starting up!
echo.
echo 📡 Backend API: http://localhost:8000
echo 🌐 Frontend App: http://localhost:3000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press any key to open the application in your browser...
pause >nul

REM Open browser
start http://localhost:3000

echo.
echo 💡 To stop the system:
echo    - Close both terminal windows
echo    - Or press Ctrl+C in each terminal
echo.
pause