'use client'

import { useState, useEffect } from 'react'
import { File, Trash2, Play, RefreshCw, CheckCircle, XCircle } from 'lucide-react'
import axios from 'axios'

interface FileInfo {
  filename: string
  original_path: string
  text_exists: boolean
  embeddings_exist: boolean
  size: number
  modified: number
}

interface FileListProps {
  refreshTrigger: number
  onRefresh: () => void
  onProcessFile: (fileId: string) => void
}

export default function FileList({ refreshTrigger, onRefresh, onProcessFile }: FileListProps) {
  const [files, setFiles] = useState<FileInfo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchFiles = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get('/api/files')
      setFiles(response.data.files)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch files')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchFiles()
  }, [refreshTrigger])

  const handleDelete = async (filename: string) => {
    if (!confirm(`Are you sure you want to delete "${filename}" and all associated files?`)) {
      return
    }

    try {
      await axios.delete(`/api/files/${encodeURIComponent(filename)}`)
      onRefresh()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to delete file')
    }
  }

  const handleProcess = async (filename: string) => {
    try {
      const response = await axios.post(`/api/process-local/${encodeURIComponent(filename)}`)
      if (response.data.status === 'success') {
        onProcessFile(response.data.file_id)
      }
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to start processing')
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString()
  }

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
          <span className="ml-3 text-gray-600">Loading files...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center py-8">
          <XCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 font-medium">{error}</p>
          <button
            onClick={fetchFiles}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-md">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">
            📁 Document Files ({files.length})
          </h3>
          <button
            onClick={onRefresh}
            className="flex items-center px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </button>
        </div>
      </div>

      {files.length === 0 ? (
        <div className="p-8 text-center">
          <File className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No files found</p>
          <p className="text-sm text-gray-500 mt-1">
            Upload files or place them in the Documents folder
          </p>
        </div>
      ) : (
        <div className="divide-y divide-gray-200">
          {files.map((file) => (
            <div key={file.filename} className="p-6 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center">
                    <File className="w-5 h-5 text-gray-400 mr-3 flex-shrink-0" />
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {file.filename}
                      </p>
                      <div className="flex items-center mt-1 space-x-4 text-xs text-gray-500">
                        <span>{formatFileSize(file.size)}</span>
                        <span>{formatDate(file.modified)}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-4 ml-4">
                  {/* Status Indicators */}
                  <div className="flex items-center space-x-2">
                    <div className="flex items-center">
                      {file.text_exists ? (
                        <CheckCircle className="w-4 h-4 text-green-500" />
                      ) : (
                        <XCircle className="w-4 h-4 text-gray-300" />
                      )}
                      <span className="text-xs text-gray-600 ml-1">Text</span>
                    </div>
                    <div className="flex items-center">
                      {file.embeddings_exist ? (
                        <CheckCircle className="w-4 h-4 text-green-500" />
                      ) : (
                        <XCircle className="w-4 h-4 text-gray-300" />
                      )}
                      <span className="text-xs text-gray-600 ml-1">Embeddings</span>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center space-x-2">
                    {!file.embeddings_exist && (
                      <button
                        onClick={() => handleProcess(file.filename)}
                        className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        title="Process file"
                      >
                        <Play className="w-4 h-4" />
                      </button>
                    )}
                    <button
                      onClick={() => handleDelete(file.filename)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete file"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}