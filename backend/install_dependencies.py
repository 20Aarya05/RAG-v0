#!/usr/bin/env python3
"""
Automated dependency installer for RAG Backend
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected. Python 3.8+ required.")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_tesseract():
    """Check if Tesseract OCR is installed"""
    tesseract_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        "tesseract"  # If in PATH
    ]
    
    for path in tesseract_paths:
        try:
            if os.path.exists(path) or path == "tesseract":
                subprocess.run([path, "--version"], capture_output=True, check=True)
                print(f"✅ Tesseract OCR found at: {path}")
                return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    print("❌ Tesseract OCR not found!")
    print("💡 Please install Tesseract OCR:")
    print("   Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
    print("   Linux: sudo apt-get install tesseract-ocr")
    print("   Mac: brew install tesseract")
    return False

def install_core_dependencies():
    """Install core dependencies"""
    commands = [
        ("python -m pip install --upgrade pip", "Upgrading pip"),
        ("pip install -r requirements.txt", "Installing core dependencies")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def install_optional_dependencies():
    """Install optional dependencies with user choice"""
    optional_deps = {
        "sentence-transformers": {
            "description": "HuggingFace embeddings (local, high-quality)",
            "command": "pip install sentence-transformers",
            "size": "~500MB (includes PyTorch)"
        },
        "fastapi": {
            "description": "Web API framework (for future API endpoints)",
            "command": "pip install fastapi uvicorn",
            "size": "~50MB"
        },
        "development": {
            "description": "Development tools (testing, formatting)",
            "command": "pip install pytest black flake8",
            "size": "~30MB"
        }
    }
    
    print("\n🔧 Optional Dependencies:")
    print("=" * 50)
    
    for name, info in optional_deps.items():
        print(f"\n📦 {name.upper()}:")
        print(f"   Description: {info['description']}")
        print(f"   Size: {info['size']}")
        
        choice = input(f"   Install {name}? (y/N): ").strip().lower()
        if choice in ['y', 'yes']:
            run_command(info['command'], f"Installing {name}")

def test_installation():
    """Test if key imports work"""
    print("\n🧪 Testing Installation:")
    print("=" * 30)
    
    test_imports = [
        ("fitz", "PyMuPDF (PDF processing)"),
        ("docx", "python-docx (DOCX processing)"),
        ("pptx", "python-pptx (PowerPoint processing)"),
        ("PIL", "Pillow (Image processing)"),
        ("pytesseract", "pytesseract (OCR)"),
        ("requests", "requests (HTTP client)"),
        ("numpy", "numpy (Numerical computing)")
    ]
    
    failed_imports = []
    
    for module, description in test_imports:
        try:
            __import__(module)
            print(f"✅ {description}")
        except ImportError:
            print(f"❌ {description}")
            failed_imports.append(module)
    
    # Test optional imports
    optional_imports = [
        ("sentence_transformers", "sentence-transformers (HuggingFace embeddings)"),
        ("fastapi", "FastAPI (Web framework)"),
        ("pytest", "pytest (Testing framework)")
    ]
    
    print("\n🔍 Optional Dependencies:")
    for module, description in optional_imports:
        try:
            __import__(module)
            print(f"✅ {description}")
        except ImportError:
            print(f"⚠️  {description} (optional)")
    
    if failed_imports:
        print(f"\n❌ Failed imports: {', '.join(failed_imports)}")
        print("💡 Try running: pip install -r requirements.txt")
        return False
    else:
        print("\n🎉 All core dependencies installed successfully!")
        return True

def main():
    """Main installation process"""
    print("🚀 RAG Backend Dependency Installer")
    print("=" * 40)
    
    # Check prerequisites
    if not check_python_version():
        return
    
    if not check_tesseract():
        print("\n⚠️  Continuing without Tesseract (OCR features will be limited)")
    
    # Install core dependencies
    print(f"\n📦 Installing Core Dependencies...")
    if not install_core_dependencies():
        print("❌ Core dependency installation failed!")
        return
    
    # Install optional dependencies
    install_optional_dependencies()
    
    # Test installation
    test_installation()
    
    print("\n🎯 Next Steps:")
    print("1. Test the installation: python File_entry.py")
    print("2. Configure embeddings: python configure_embeddings.py")
    print("3. Process documents: python batch_processor.py")
    
    print("\n📚 Documentation:")
    print("• For OpenAI embeddings: Set OPENAI_API_KEY environment variable")
    print("• For HuggingFace embeddings: Models download automatically")
    print("• For OCR features: Ensure Tesseract is installed and in PATH")

if __name__ == "__main__":
    main()