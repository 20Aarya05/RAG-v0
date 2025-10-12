#!/usr/bin/env python3
"""
Test script to verify API server file upload functionality
"""

import requests
import time
import os
from pathlib import Path

def test_api_upload():
    """Test file upload via API"""
    
    # API endpoint
    base_url = "http://localhost:8000"
    
    try:
        # Test health endpoint
        print("🔍 Testing API health...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running!")
        else:
            print("❌ API server health check failed")
            return False
            
        # Test file upload
        print("📤 Testing file upload...")
        test_file = "backend/RAG-embedding/Documents/CS_Module_01.pdf"
        
        if not os.path.exists(test_file):
            print(f"❌ Test file not found: {test_file}")
            return False
            
        with open(test_file, 'rb') as f:
            files = {'file': ('CS_Module_01.pdf', f, 'application/pdf')}
            response = requests.post(f"{base_url}/upload", files=files, timeout=30)
            
        if response.status_code == 200:
            result = response.json()
            print(f"✅ File upload successful! File ID: {result.get('file_id')}")
            
            # Check processing status
            file_id = result.get('file_id')
            if file_id:
                print("⏳ Checking processing status...")
                time.sleep(2)
                
                status_response = requests.get(f"{base_url}/status/{file_id}")
                if status_response.status_code == 200:
                    status = status_response.json()
                    print(f"📊 Processing status: {status.get('status')}")
                    print(f"💬 Message: {status.get('message')}")
                    return True
                    
        else:
            print(f"❌ File upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Make sure it's running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing API Server File Upload")
    print("=" * 40)
    
    success = test_api_upload()
    
    if success:
        print("\n🎉 API upload test completed successfully!")
    else:
        print("\n❌ API upload test failed!")
        print("\n💡 Make sure to:")
        print("   1. Start the API server: cd backend && python api_server.py")
        print("   2. Wait for it to fully start")
        print("   3. Run this test again")