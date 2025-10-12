# 🚀 START HERE - Complete RAG System Setup

## ✅ System Status

- ✅ **Python 3.12.6** - Ready
- ✅ **Node.js v22.14.0** - Ready
- ✅ **Backend Dependencies** - Installed
- ✅ **Frontend Dependencies** - Installed
- ✅ **Virtual Environment** - Ready

---

## 🎯 **QUICK START (3 Simple Steps)**

### **Option 1: Automated Startup (Recommended)**

**Just run this one command:**

```bash
start_everything.bat
```

This will:

- ✅ Check all requirements
- ✅ Start backend API server
- ✅ Start frontend development server
- ✅ Open your browser automatically

### **Option 2: Manual Startup**

**Terminal 1 - Backend:**

```bash
cd backend
.\venv\Scripts\Activate.ps1
python api_server.py
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

---

## 🌐 **Access Your Application**

Once started, open these URLs:

- **🎯 Main Application**: http://localhost:3000
- **📡 Backend API**: http://localhost:8000
- **📚 API Documentation**: http://localhost:8000/docs

---

## 📋 **How to Use the System**

### **Web Interface (Recommended)**

1. **Upload Files**: Go to Upload tab, drag & drop PDF/DOCX/PPTX files
2. **Monitor Progress**: Check Status tab for real-time processing updates
3. **Manage Files**: Use Files tab to view/delete processed documents
4. **Configure**: Check Config tab for embedding settings

### **Manual Processing (Still Available)**

1. Place files in `backend/RAG-embedding/Documents/`
2. Run: `cd backend/RAG-embedding && python File_entry.py`

---

## 🔧 **Supported File Types**

- **PDF** - Text extraction + OCR for scanned PDFs
- **DOCX/DOC** - Microsoft Word documents
- **PPTX/PPT** - PowerPoint presentations

---

## 🛠️ **Troubleshooting**

### **If something doesn't work:**

1. **Run the test script:**

   ```bash
   python test_setup.py
   ```

2. **Check if services are running:**

   - Backend: http://localhost:8000 (should show JSON)
   - Frontend: http://localhost:3000 (should show web interface)

3. **Common fixes:**

   ```bash
   # Restart everything
   # Close both terminals, then run:
   start_everything.bat

   # Or check what's using the ports:
   netstat -ano | findstr :3000
   netstat -ano | findstr :8000
   ```

### **Port conflicts:**

If ports 3000 or 8000 are busy:

```bash
# Use different ports
cd frontend
npm run dev -- -p 3001  # Frontend on port 3001

# Backend will auto-find available port
```

---

## 📊 **System Architecture**

```
┌─────────────────┐    HTTP/API    ┌──────────────────┐
│   Frontend      │◄──────────────►│    Backend       │
│   (React/Next)  │                │   (Python/API)   │
│   Port 3000     │                │   Port 8000      │
└─────────────────┘                └──────────────────┘
                                            │
                                            ▼
                                   ┌──────────────────┐
                                   │  File Processing │
                                   │  (Your existing  │
                                   │   File_entry.py) │
                                   └──────────────────┘
```

---

## 🎉 **What You Get**

### **Modern Web Interface:**

- Drag & drop file upload
- Real-time processing status
- File management dashboard
- Configuration panel

### **Powerful Backend:**

- REST API for all operations
- Background file processing
- Multiple embedding providers
- Full compatibility with existing code

### **Flexible Usage:**

- Web upload + processing
- Manual file processing (unchanged)
- API access for automation
- Real-time status monitoring

---

## 💡 **Pro Tips**

1. **Keep terminals open** while using the system
2. **Check logs** in both terminals for any errors
3. **Use browser dev tools** (F12) to debug frontend issues
4. **API docs** at http://localhost:8000/docs are interactive
5. **Files persist** - uploaded files stay in Documents folder

---

## 🆘 **Need Help?**

**Quick Diagnostics:**

```bash
# Test everything
python test_setup.py

# Check Python environment
cd backend
.\venv\Scripts\Activate.ps1
python -c "import fastapi; print('Backend OK')"

# Check Node.js environment
cd frontend
npm run build
```

**Check System Status:**

- Backend health: http://localhost:8000
- Frontend: http://localhost:3000
- Both should respond without errors

---

## 🔄 **Daily Usage**

**To Start System:**

```bash
start_everything.bat
```

**To Stop System:**

- Close both terminal windows, or
- Press `Ctrl+C` in each terminal

**To Use:**

1. Open http://localhost:3000
2. Upload files or use manual processing
3. Monitor progress and manage files

---

## 🎯 **Ready to Go!**

Your RAG system is fully configured and ready to use. The web interface provides an easy way to upload and process documents, while maintaining full compatibility with your existing manual processing workflow.

**Start now:** Run `start_everything.bat` and open http://localhost:3000

Happy document processing! 🚀
