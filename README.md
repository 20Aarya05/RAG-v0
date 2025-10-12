# RAG Document Processing System

A complete full-stack solution for processing documents and generating embeddings for Retrieval-Augmented Generation (RAG) applications.

## 🌟 Features

### Frontend (React/Next.js)

- 📤 **Drag & Drop Upload** - Easy file upload interface
- 📁 **File Management** - View, process, and delete documents
- ⚡ **Real-time Status** - Live processing updates with progress bars
- ⚙️ **Configuration Panel** - View and manage embedding settings
- 💻 **Local Processing** - Support for manual file processing

### Backend (Python/FastAPI)

- 🔄 **Multi-format Support** - PDF, DOCX, DOC, PPTX, PPT
- 🤖 **Multiple Embedding Providers** - Dummy, HuggingFace, OpenAI
- 📊 **OCR Support** - Extract text from scanned documents and images
- 🚀 **Async Processing** - Background file processing
- 📡 **REST API** - Complete API for file operations

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

1. **Clone and Setup**

   ```bash
   git clone <repository>
   cd rag-system
   ```

2. **Run Setup Script**

   ```bash
   # Windows
   setup_frontend.bat

   # Then start the system
   start_system.bat
   ```

3. **Open Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python api_server.py
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
rag-system/
├── backend/                    # Python backend
│   ├── RAG-embedding/         # Core processing modules
│   │   ├── Documents/         # Input documents
│   │   ├── Text_files/        # Extracted text
│   │   ├── Embeddings/        # Generated embeddings
│   │   ├── DOCX/             # DOCX processing
│   │   ├── PDF/              # PDF processing
│   │   ├── PPT/              # PowerPoint processing
│   │   └── Embedding_C/      # Embedding generation
│   ├── api_server.py         # FastAPI server
│   ├── requirements.txt      # Python dependencies
│   └── venv/                 # Virtual environment
├── frontend/                  # React/Next.js frontend
│   ├── app/                  # Next.js app directory
│   ├── components/           # React components
│   ├── package.json          # Node.js dependencies
│   └── next.config.js        # Next.js configuration
├── start_system.bat          # Windows startup script
├── setup_frontend.bat        # Frontend setup script
├── test_setup.py            # System test script
└── README.md                # This file
```

## 🔧 Configuration

### Embedding Providers

#### 1. Dummy Provider (Default)

- **Use case**: Testing and development
- **Setup**: No configuration needed
- **Quality**: Consistent dummy embeddings

#### 2. HuggingFace Provider

- **Use case**: Local, high-quality embeddings
- **Setup**: `pip install sentence-transformers`
- **Quality**: Good semantic understanding
- **Models**: all-MiniLM-L6-v2, all-mpnet-base-v2

#### 3. OpenAI Provider

- **Use case**: Premium quality embeddings
- **Setup**: Set `OPENAI_API_KEY` environment variable
- **Quality**: Best semantic understanding
- **Models**: text-embedding-3-small, text-embedding-3-large

### Configuration Commands

```bash
# Interactive configuration
cd backend
python configure_embeddings.py

# Test configuration
python test_embeddings.py
```

## 📋 Supported File Types

| Format     | Extension       | Features                              |
| ---------- | --------------- | ------------------------------------- |
| PDF        | `.pdf`          | Text extraction, OCR for scanned PDFs |
| Word       | `.docx`, `.doc` | Text, tables, images with OCR         |
| PowerPoint | `.pptx`, `.ppt` | Text, tables, charts, images with OCR |

## 🛠️ Usage

### Web Interface

1. **Upload Files**

   - Go to Upload tab
   - Drag & drop files or click to select
   - Automatic processing starts

2. **Monitor Progress**

   - Go to Status tab
   - View real-time processing updates
   - See completion status

3. **Manage Files**

   - Go to Files tab
   - View all processed documents
   - Delete or reprocess files

4. **Configure System**
   - Go to Config tab
   - View current settings
   - See configuration instructions

### Command Line Interface

```bash
# Process single file
cd backend/RAG-embedding
python File_entry.py

# Process all files in Documents folder
python batch_processor.py

# Configure embedding provider
python configure_embeddings.py

# Test embedding quality
python test_embeddings.py
```

### API Usage

```python
import requests

# Upload file
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/upload',
        files={'file': f}
    )

# Check status
file_id = response.json()['file_id']
status = requests.get(f'http://localhost:8000/api/status/{file_id}')

# List files
files = requests.get('http://localhost:8000/api/files')
```

## 🧪 Testing

### Run System Tests

```bash
python test_setup.py
```

### Manual Testing

```bash
# Test backend
cd backend
python -c "import fitz, docx, pptx; print('✅ All imports work')"

# Test frontend
cd frontend
npm run build
```

## 🔍 Troubleshooting

### Common Issues

**Backend won't start:**

- Activate virtual environment: `venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

**Frontend won't start:**

- Install Node.js (16+ required)
- Install dependencies: `npm install`
- Check port 3000 is available

**File processing fails:**

- Check Tesseract OCR is installed
- Verify file permissions
- Check backend logs for errors

**OCR not working:**

- Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Update path in Python files if needed

### Getting Help

1. **Check Logs**

   - Backend: Console output where `api_server.py` is running
   - Frontend: Browser console (F12)

2. **Run Tests**

   ```bash
   python test_setup.py
   ```

3. **Verify Setup**
   - Check all dependencies are installed
   - Ensure virtual environment is activated
   - Verify file paths and permissions

## 🚀 Production Deployment

### Backend

```bash
# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api_server:app

# Or use Docker
docker build -t rag-backend .
docker run -p 8000:8000 rag-backend
```

### Frontend

```bash
# Build for production
npm run build
npm run start

# Or use static export
npm run build && npm run export
```

### Environment Variables

```bash
# Backend
export OPENAI_API_KEY=your_key_here
export ENVIRONMENT=production

# Frontend
export NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

## 📊 Performance

### Processing Times (Approximate)

- **Small PDF (1-5 pages)**: 10-30 seconds
- **Large PDF (50+ pages)**: 2-5 minutes
- **DOCX with images**: 30-60 seconds
- **PowerPoint**: 20-40 seconds

### Embedding Generation

- **Dummy**: Instant
- **HuggingFace**: 1-5 seconds per chunk
- **OpenAI**: 0.5-2 seconds per chunk (API dependent)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test
4. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **PyMuPDF** - PDF processing
- **python-docx** - Word document processing
- **python-pptx** - PowerPoint processing
- **Tesseract OCR** - Optical character recognition
- **HuggingFace** - Transformer models
- **OpenAI** - Embedding API
- **FastAPI** - Backend framework
- **Next.js** - Frontend framework
- **Tailwind CSS** - Styling

---

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Run `python test_setup.py` to diagnose issues
3. Check existing issues in the repository
4. Create a new issue with detailed information

**Happy document processing! 🚀**
