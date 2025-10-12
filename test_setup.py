#!/usr/bin/env python3
"""
Test script to verify RAG system setup
"""

import os
import sys
import subprocess
import requests
import time

def test_python_dependencies():
    """Test if Python dependencies are installed"""
    print("🧪 Testing Python Dependencies...")
    
    required_modules = [
        'fastapi',
        'uvicorn', 
        'fitz',  # PyMuPDF
        'docx',  # python-docx
        'pptx',  # python-pptx
        'PIL',   # Pillow
        'pytesseract',
        'requests',
        'numpy'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    print("✅ All Python dependencies found!")
    return True

def test_backend_structure():
    """Test if backend file structure is correct"""
    print("\n🧪 Testing Backend Structure...")
    
    required_paths = [
        'backend/RAG-embedding/File_entry.py',
        'backend/RAG-embedding/embedding_config.py',
        'backend/RAG-embedding/Embedding_C/Text_To_Embeddings.py',
        'backend/RAG-embedding/Documents',
        'backend/api_server.py'
    ]
    
    missing_paths = []
    
    for path in required_paths:
        if os.path.exists(path):
            print(f"  ✅ {path}")
        else:
            print(f"  ❌ {path}")
            missing_paths.append(path)
    
    if missing_paths:
        print(f"\n❌ Missing paths: {', '.join(missing_paths)}")
        return False
    
    print("✅ Backend structure is correct!")
    return True

def test_frontend_structure():
    """Test if frontend structure is correct"""
    print("\n🧪 Testing Frontend Structure...")
    
    required_paths = [
        'frontend/package.json',
        'frontend/app/page.tsx',
        'frontend/components/FileUpload.tsx',
        'frontend/next.config.js'
    ]
    
    missing_paths = []
    
    for path in required_paths:
        if os.path.exists(path):
            print(f"  ✅ {path}")
        else:
            print(f"  ❌ {path}")
            missing_paths.append(path)
    
    if missing_paths:
        print(f"\n❌ Missing paths: {', '.join(missing_paths)}")
        return False
    
    print("✅ Frontend structure is correct!")
    return True

def test_node_dependencies():
    """Test if Node.js and npm are available"""
    print("\n🧪 Testing Node.js Dependencies...")
    
    try:
        # Check Node.js
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ Node.js: {result.stdout.strip()}")
        else:
            print("  ❌ Node.js not found")
            return False
        
        # Check npm
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ npm: {result.stdout.strip()}")
        else:
            print("  ❌ npm not found")
            return False
        
        # Check if frontend dependencies are installed
        if os.path.exists('frontend/node_modules'):
            print("  ✅ Frontend dependencies installed")
        else:
            print("  ⚠️  Frontend dependencies not installed")
            print("     Run: cd frontend && npm install")
        
        return True
        
    except FileNotFoundError:
        print("  ❌ Node.js/npm not found")
        print("💡 Install Node.js from https://nodejs.org/")
        return False

def test_api_server():
    """Test if API server can start"""
    print("\n🧪 Testing API Server...")
    
    # Try to start the server in background
    try:
        os.chdir('backend')
        process = subprocess.Popen([
            sys.executable, 'api_server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Test if server is responding
        try:
            response = requests.get('http://localhost:8000/', timeout=5)
            if response.status_code == 200:
                print("  ✅ API server started successfully")
                print("  ✅ Health check passed")
                success = True
            else:
                print(f"  ❌ API server returned status {response.status_code}")
                success = False
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Cannot connect to API server: {e}")
            success = False
        
        # Stop the server
        process.terminate()
        process.wait(timeout=5)
        
        os.chdir('..')
        return success
        
    except Exception as e:
        print(f"  ❌ Failed to start API server: {e}")
        os.chdir('..')
        return False

def main():
    """Run all tests"""
    print("🚀 RAG System Setup Test")
    print("=" * 30)
    
    tests = [
        ("Python Dependencies", test_python_dependencies),
        ("Backend Structure", test_backend_structure),
        ("Frontend Structure", test_frontend_structure),
        ("Node.js Dependencies", test_node_dependencies),
        ("API Server", test_api_server)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 30)
    print("📊 Test Results Summary")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your RAG system is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Run: start_system.bat (Windows) to start both frontend and backend")
        print("2. Or manually:")
        print("   - Backend: cd backend && python api_server.py")
        print("   - Frontend: cd frontend && npm run dev")
        print("3. Open: http://localhost:3000")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please fix the issues above.")
        print("\n💡 Common fixes:")
        print("- Install missing Python packages: pip install -r backend/requirements.txt")
        print("- Install Node.js from: https://nodejs.org/")
        print("- Install frontend packages: cd frontend && npm install")
        print("- Check file paths and permissions")

if __name__ == "__main__":
    main()