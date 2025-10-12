@echo off
title RAG System - Quick Setup
color 0B

echo.
echo ========================================
echo 🔧 RAG System - Quick Setup
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo ❌ Error: Run this from the RAG project root directory
    pause
    exit /b 1
)

echo ✅ In correct directory: %CD%
echo.

REM Setup frontend dependencies
echo 📦 Setting up frontend dependencies...
cd frontend

if exist "node_modules" (
    echo ✅ Frontend dependencies already installed
) else (
    echo 🔄 Installing frontend dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install frontend dependencies
        cd ..
        pause
        exit /b 1
    )
    echo ✅ Frontend dependencies installed successfully
)

cd ..

REM Check backend virtual environment
echo.
echo 🐍 Checking backend setup...

if exist "backend\venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found
) else (
    echo ❌ Virtual environment not found
    echo 💡 Please run backend setup first
    pause
    exit /b 1
)

REM Test backend dependencies
cd backend
call venv\Scripts\activate.bat

echo 🔄 Testing backend dependencies...
python -c "import fastapi, uvicorn; print('✅ FastAPI and Uvicorn installed')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Backend dependencies missing
    echo 🔄 Installing backend dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install backend dependencies
        cd ..
        pause
        exit /b 1
    )
)

python -c "import fitz, docx, pptx; print('✅ Document processing libraries installed')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Some document processing libraries may be missing
    echo 💡 This might affect file processing capabilities
)

cd ..

echo.
echo ========================================
echo 🎉 Setup Complete!
echo ========================================
echo.
echo 🚀 Ready to start the system!
echo.
echo 📋 Next steps:
echo    1. Run: start_everything.bat
echo    2. Or manually start:
echo       • Backend: cd backend && venv\Scripts\activate && python api_server.py
echo       • Frontend: cd frontend && npm run dev
echo    3. Open: http://localhost:3000
echo.
echo 🧪 To test the setup: python test_setup.py
echo.

pause