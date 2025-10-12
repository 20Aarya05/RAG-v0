@echo off
echo 🚀 Setting up RAG Frontend
echo ==========================

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found!
    echo 💡 Please install Node.js from https://nodejs.org/
    echo    Recommended version: 18.x or higher
    pause
    exit /b 1
)

echo ✅ Node.js found: 
node --version

REM Navigate to frontend directory
cd frontend

REM Install dependencies
echo.
echo 📦 Installing frontend dependencies...
npm install

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✅ Frontend setup complete!
echo.
echo 🎯 Next steps:
echo 1. Start the backend: cd ../backend && python api_server.py
echo 2. Start the frontend: npm run dev
echo 3. Open http://localhost:3000
echo.
echo Or use the start_system.bat script to start both automatically
echo.
pause