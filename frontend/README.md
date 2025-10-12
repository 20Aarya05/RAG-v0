# RAG Frontend - React/Next.js

A modern web interface for uploading and processing documents for RAG (Retrieval-Augmented Generation) embeddings.

## Features

- 📤 **File Upload**: Drag & drop interface for PDF, DOCX, PPTX files
- 📁 **File Management**: View, process, and delete uploaded documents
- ⚡ **Real-time Status**: Live processing status with progress bars
- ⚙️ **Configuration**: View and manage embedding provider settings
- 💻 **Local Processing**: Support for manual local file processing

## Quick Start

### 1. Install Dependencies

```bash
npm install
# or
yarn install
```

### 2. Start Development Server

```bash
npm run dev
# or
yarn dev
```

### 3. Start Backend API

In a separate terminal:

```bash
cd ../backend
python api_server.py
```

### 4. Open Application

Visit [http://localhost:3000](http://localhost:3000)

## Project Structure

```
frontend/
├── app/                    # Next.js 13+ app directory
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # UI components
│   ├── FileUpload.tsx    # File upload component
│   ├── FileList.tsx      # File management
│   ├── ProcessingStatus.tsx # Status monitoring
│   └── ConfigPanel.tsx   # Configuration panel
├── package.json          # Dependencies
├── next.config.js        # Next.js configuration
└── tailwind.config.js    # Tailwind CSS config
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Configuration

### Environment Variables

Create `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=RAG Document Processor
```

### API Endpoints

The frontend connects to these backend endpoints:

- `POST /api/upload` - Upload files
- `GET /api/files` - List files
- `GET /api/status/{id}` - Get processing status
- `GET /api/config` - Get configuration
- `DELETE /api/files/{filename}` - Delete files

## Supported File Types

- **PDF** - Portable Document Format
- **DOCX** - Microsoft Word documents
- **DOC** - Legacy Word documents
- **PPTX** - PowerPoint presentations
- **PPT** - Legacy PowerPoint files

## Usage

### Upload Files

1. Go to the **Upload** tab
2. Drag & drop files or click to select
3. Files are automatically processed in the background

### Monitor Processing

1. Go to the **Status** tab
2. View real-time progress of file processing
3. See completion status and results

### Manage Files

1. Go to the **Files** tab
2. View all uploaded documents
3. See processing status (Text extracted, Embeddings created)
4. Delete files or reprocess them

### Configure Embeddings

1. Go to the **Config** tab
2. View current embedding provider settings
3. See instructions for changing providers

## Local Processing

For manual processing without the web interface:

1. Place files in `backend/RAG-embedding/Documents/`
2. Run processing scripts:

   ```bash
   # Single file
   python File_entry.py

   # All files
   python batch_processor.py

   # Configure embeddings
   python configure_embeddings.py
   ```

## Troubleshooting

### Common Issues

**Frontend won't start:**

- Check Node.js version (requires 16+)
- Run `npm install` to install dependencies

**Can't connect to backend:**

- Ensure backend API is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`

**File upload fails:**

- Check file type is supported
- Ensure backend has write permissions
- Check backend logs for errors

**Processing stuck:**

- Check backend console for error messages
- Verify embedding provider configuration
- Ensure required dependencies are installed

### Getting Help

1. Check browser console for errors
2. Check backend logs in terminal
3. Verify all dependencies are installed
4. Ensure virtual environment is activated for backend

## Development

### Adding New Features

1. **New Components**: Add to `components/` directory
2. **New Pages**: Add to `app/` directory (Next.js 13+ app router)
3. **Styling**: Use Tailwind CSS classes
4. **API Calls**: Use axios for HTTP requests

### Code Style

- TypeScript for type safety
- Tailwind CSS for styling
- ESLint for code quality
- Functional components with hooks

## Production Deployment

### Build for Production

```bash
npm run build
npm run start
```

### Environment Setup

- Set production API URL in environment variables
- Configure CORS in backend for production domain
- Use process manager (PM2) for backend
- Use reverse proxy (nginx) for serving

## License

This project is part of the RAG Backend system.
