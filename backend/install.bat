@echo off
echo 🚀 RAG Backend - Quick Installation
echo =====================================

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo 🔄 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  No virtual environment found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo.
echo 📦 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 🧪 Testing installation...
python install_dependencies.py

echo.
echo ✅ Installation complete!
echo.
echo 🎯 Next steps:
echo 1. Run: python File_entry.py
echo 2. Configure: python configure_embeddings.py
echo.
pause