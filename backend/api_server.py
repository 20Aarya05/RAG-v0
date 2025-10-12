#!/usr/bin/env python3
"""
FastAPI server for RAG Backend - File Upload and Processing API
"""

import os
import shutil
import json
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import your existing modules
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'RAG-embedding'))

try:
    from File_entry import process_file
    from embedding_config import get_embedding_config
    import Embedding_C.Text_To_Embeddings as Text_To_Embeddings
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the backend directory")
    print("💡 And that RAG-embedding folder exists with all modules")
    sys.exit(1)

app = FastAPI(
    title="RAG Backend API",
    description="File upload and processing API for RAG system",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_DIR = Path("RAG-embedding/Documents")
TEXT_DIR = Path("RAG-embedding/Text_files")
EMBEDDINGS_DIR = Path("RAG-embedding/Embeddings")

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
TEXT_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

# Supported file types
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".pptx", ".ppt"}

# Store processing status
processing_status = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "RAG Backend API is running", "status": "healthy"}

@app.get("/api/config")
async def get_config():
    """Get current embedding configuration"""
    try:
        config = get_embedding_config()
        return {
            "status": "success",
            "config": config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get config: {str(e)}")

@app.post("/api/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """Upload and process a file"""
    
    # Validate file type
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {file_ext}. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
        )
    
    # Generate unique filename to avoid conflicts
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    safe_filename = f"{Path(file.filename).stem}_{unique_id}{file_ext}"
    file_path = UPLOAD_DIR / safe_filename
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Initialize processing status
        processing_status[unique_id] = {
            "status": "uploaded",
            "filename": file.filename,
            "safe_filename": safe_filename,
            "progress": 0,
            "message": "File uploaded successfully"
        }
        
        # Start background processing with original filename
        background_tasks.add_task(process_uploaded_file, unique_id, str(file_path), file.filename)
        
        return {
            "status": "success",
            "message": "File uploaded and processing started",
            "file_id": unique_id,
            "filename": file.filename
        }
        
    except Exception as e:
        # Clean up file if processing fails
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

async def process_uploaded_file(file_id: str, file_path: str, original_filename: str):
    """Background task to process uploaded file"""
    try:
        # Update status
        processing_status[file_id]["status"] = "processing"
        processing_status[file_id]["progress"] = 25
        processing_status[file_id]["message"] = "Processing file (text extraction + embeddings)..."
        
        # Use original filename for output files (without extension)
        original_base_name = Path(original_filename).stem
        
        # Process file (extract text + generate embeddings) with custom output name
        success = process_file(file_path, generate_embeddings=True, output_base_name=original_base_name)
        if not success:
            processing_status[file_id]["status"] = "error"
            processing_status[file_id]["message"] = "Failed to process file"
            return
        
        # Verify output files were created with original names
        text_file_path = TEXT_DIR / f"{original_base_name}.txt"
        embeddings_file_path = EMBEDDINGS_DIR / f"{original_base_name}.json"
        
        if not text_file_path.exists():
            processing_status[file_id]["status"] = "error"
            processing_status[file_id]["message"] = "Text file not found after processing"
            return
            
        if not embeddings_file_path.exists():
            processing_status[file_id]["status"] = "error"
            processing_status[file_id]["message"] = "Embeddings file not found after processing"
            return
        
        embeddings_path = str(embeddings_file_path)
        
        # Success
        processing_status[file_id]["status"] = "completed"
        processing_status[file_id]["progress"] = 100
        processing_status[file_id]["message"] = "Processing completed successfully"
        processing_status[file_id]["text_file"] = str(text_file_path)
        processing_status[file_id]["embeddings_file"] = embeddings_path
        
    except Exception as e:
        processing_status[file_id]["status"] = "error"
        processing_status[file_id]["message"] = f"Processing failed: {str(e)}"

@app.get("/api/status/{file_id}")
async def get_processing_status(file_id: str):
    """Get processing status for a file"""
    if file_id not in processing_status:
        raise HTTPException(status_code=404, detail="File ID not found")
    
    return {
        "status": "success",
        "data": processing_status[file_id]
    }

@app.get("/api/files")
async def list_files():
    """List all processed files"""
    try:
        files = []
        
        # List documents
        for doc_file in UPLOAD_DIR.glob("*"):
            if doc_file.suffix.lower() in SUPPORTED_EXTENSIONS:
                base_name = doc_file.stem
                text_file = TEXT_DIR / f"{base_name}.txt"
                embeddings_file = EMBEDDINGS_DIR / f"{base_name}.json"
                
                files.append({
                    "filename": doc_file.name,
                    "original_path": str(doc_file),
                    "text_exists": text_file.exists(),
                    "embeddings_exist": embeddings_file.exists(),
                    "size": doc_file.stat().st_size if doc_file.exists() else 0,
                    "modified": doc_file.stat().st_mtime if doc_file.exists() else 0
                })
        
        return {
            "status": "success",
            "files": files
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

@app.delete("/api/files/{filename}")
async def delete_file(filename: str):
    """Delete a file and its associated text/embeddings"""
    try:
        # Find and delete original file
        doc_file = UPLOAD_DIR / filename
        if doc_file.exists():
            doc_file.unlink()
        
        # Delete associated files
        base_name = Path(filename).stem
        text_file = TEXT_DIR / f"{base_name}.txt"
        embeddings_file = EMBEDDINGS_DIR / f"{base_name}.json"
        
        if text_file.exists():
            text_file.unlink()
        if embeddings_file.exists():
            embeddings_file.unlink()
        
        return {
            "status": "success",
            "message": f"File {filename} and associated files deleted"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@app.post("/api/process-local/{filename}")
async def process_local_file(filename: str, background_tasks: BackgroundTasks):
    """Process a file that's already in the Documents folder"""
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Generate processing ID
    import uuid
    file_id = str(uuid.uuid4())[:8]
    
    # Initialize processing status
    processing_status[file_id] = {
        "status": "processing",
        "filename": filename,
        "safe_filename": filename,
        "progress": 0,
        "message": "Starting local file processing..."
    }
    
    # Start background processing
    background_tasks.add_task(process_uploaded_file, file_id, str(file_path))
    
    return {
        "status": "success",
        "message": "Local file processing started",
        "file_id": file_id,
        "filename": filename
    }

if __name__ == "__main__":
    print("🚀 Starting RAG Backend API Server...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 CORS enabled for: http://localhost:3000")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )