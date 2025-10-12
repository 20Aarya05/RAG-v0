# 🚀 Complete Startup Guide - RAG System

## Prerequisites ✅

- ✅ Python 3.12.6 (Detected)
- ✅ Node.js v22.14.0 (Detected)
- ✅ Virtual environment exists in `backend/venv`

## 🎯 Quick Start (3 Steps)

### **Step 1: Setup Frontend Dependencies**

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies (one-time setup)
npm install
```

### **Step 2: Start Backend API Server**

```bash
# Open Terminal 1 - Navigate to backend
cd backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start the API server
python api_server.py
```

### **Step 3: Start Frontend Development Server**

```bash
# Open Terminal 2 - Navigate to frontend
cd frontend

# Start the development server
npm run dev
```

### **Step 4: Access the Application**

- 🌐 **Frontend**: http://localhost:3000
- 📡 **Backend API**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs

---

## 🔧 Detailed Instructions

### **Terminal 1: Backend Setup**

```powershell
# 1. Navigate to project root
cd "D:\C Documents\VS CODE CODES\RAG"

# 2. Go to backend directory
cd backend

# 3. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 4. Verify dependencies (should already be installed)
pip list | findstr fastapi

# 5. Start the API server
python api_server.py
```

**Expected Output:**

```
🚀 Starting RAG Backend API Server...
📡 API will be available at: http://localhost:8000
📚 API Documentation: http://localhost:8000/docs
🔄 CORS enabled for: http://localhost:3000
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### **Terminal 2: Frontend Setup**

```powershell
# 1. Open NEW terminal/command prompt
# 2. Navigate to project root
cd "D:\C Documents\VS CODE CODES\RAG"

# 3. Go to frontend directory
cd frontend

# 4. Install dependencies (first time only)
npm install

# 5. Start development server
npm run dev
```

**Expected Output:**

```
> rag-frontend@0.1.0 dev
> next dev

   ▲ Next.js 14.0.0
   - Local:        http://localhost:3000
   - Environments: .env.local

 ✓ Ready in 2.1s
```

---

## 🛠️ Troubleshooting

### **Backend Issues**

**Problem: "Module not found" error**

```bash
# Solution: Check if you're in the right directory
cd backend
.\venv\Scripts\Activate.ps1
python -c "import sys; print(sys.path)"
```

**Problem: "Port 8000 already in use"**

```bash
# Solution: Kill existing process
netstat -ano | findstr :8000
# Find PID and kill it
taskkill /PID <PID_NUMBER> /F
```

**Problem: Virtual environment not activating**

```bash
# Solution: Recreate virtual environment
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### **Frontend Issues**

**Problem: "npm not found"**

- Install Node.js from https://nodejs.org/

**Problem: "Port 3000 already in use"**

```bash
# Solution: Use different port
npm run dev -- -p 3001
# Then access at http://localhost:3001
```

**Problem: Dependencies not installing**

```bash
# Solution: Clear cache and reinstall
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

## 🧪 Test Everything is Working

### **1. Test Backend API**

Open browser: http://localhost:8000
Should see: `{"message": "RAG Backend API is running", "status": "healthy"}`

### **2. Test API Documentation**

Open browser: http://localhost:8000/docs
Should see: Interactive API documentation

### **3. Test Frontend**

Open browser: http://localhost:3000
Should see: RAG Document Processor interface

### **4. Test File Upload**

1. Go to Upload tab
2. Try uploading a PDF/DOCX file
3. Check Status tab for processing progress

---

## 📁 Directory Structure Check

Your structure should look like this:

```
D:\C Documents\VS CODE CODES\RAG\
├── backend/
│   ├── venv/                     # Virtual environment
│   ├── RAG-embedding/           # Your existing code
│   │   ├── Documents/           # Input files
│   │   ├── Text_files/          # Extracted text
│   │   ├── Embeddings/          # Generated embeddings
│   │   └── File_entry.py        # Your main processing file
│   ├── api_server.py            # New API server
│   └── requirements.txt         # Dependencies
├── frontend/
│   ├── app/                     # Next.js pages
│   ├── components/              # React components
│   ├── package.json             # Node dependencies
│   └── node_modules/            # Installed packages
└── README.md                    # Documentation
```

---

## 🎯 Usage Workflow

### **Web Interface Workflow:**

1. **Upload**: Drag & drop files in Upload tab
2. **Monitor**: Watch progress in Status tab
3. **Manage**: View/delete files in Files tab
4. **Configure**: Check settings in Config tab

### **Manual Processing (Still Works):**

1. Place files in `backend/RAG-embedding/Documents/`
2. Run: `python File_entry.py`
3. Files processed as before

---

## 🔄 Daily Startup Routine

**Every time you want to use the system:**

1. **Start Backend** (Terminal 1):

   ```bash
   cd backend
   .\venv\Scripts\Activate.ps1
   python api_server.py
   ```

2. **Start Frontend** (Terminal 2):

   ```bash
   cd frontend
   npm run dev
   ```

3. **Open Browser**: http://localhost:3000

**To Stop:**

- Press `Ctrl+C` in both terminals
- Or close the terminal windows

---

## 💡 Pro Tips

1. **Keep terminals open** - Don't close them while using the system
2. **Check logs** - Both terminals show useful error messages
3. **Use browser dev tools** - F12 to see frontend errors
4. **API docs are helpful** - http://localhost:8000/docs for testing
5. **Files persist** - Uploaded files stay in Documents folder

---

## 🆘 Need Help?

**Run the test script:**

```bash
python test_setup.py
```

**Check if everything is running:**

- Backend: http://localhost:8000 (should show JSON response)
- Frontend: http://localhost:3000 (should show web interface)
- API Docs: http://localhost:8000/docs (should show documentation)

**Common Commands:**

```bash
# Check what's running on ports
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Restart everything
# Ctrl+C in both terminals, then restart
```
