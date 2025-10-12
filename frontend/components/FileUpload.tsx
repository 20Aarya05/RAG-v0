'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, File, AlertCircle, CheckCircle } from 'lucide-react'
import axios from 'axios'

interface FileUploadProps {
  onFileUploaded: (fileId: string) => void
}

export default function FileUpload({ onFileUploaded }: FileUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<{
    type: 'success' | 'error' | null
    message: string
  }>({ type: null, message: '' })

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return

    const file = acceptedFiles[0]
    setUploading(true)
    setUploadStatus({ type: null, message: '' })

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      if (response.data.status === 'success') {
        setUploadStatus({
          type: 'success',
          message: `File "${file.name}" uploaded successfully!`
        })
        onFileUploaded(response.data.file_id)
      }
    } catch (error: any) {
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || 'Upload failed'
      })
    } finally {
      setUploading(false)
    }
  }, [onFileUploaded])

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
      'application/vnd.ms-powerpoint': ['.ppt']
    },
    maxFiles: 1,
    disabled: uploading
  })

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
          }
          ${uploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <div className="space-y-4">
          {uploading ? (
            <div className="animate-spin mx-auto w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full"></div>
          ) : (
            <Upload className="mx-auto w-12 h-12 text-gray-400" />
          )}
          
          <div>
            <p className="text-lg font-medium text-gray-900">
              {uploading 
                ? 'Uploading...' 
                : isDragActive 
                  ? 'Drop the file here' 
                  : 'Drag & drop a file here'
              }
            </p>
            <p className="text-sm text-gray-500 mt-1">
              or click to select a file
            </p>
          </div>
          
          <div className="text-xs text-gray-400">
            Supported: PDF, DOCX, DOC, PPTX, PPT (Max 100MB)
          </div>
        </div>
      </div>

      {/* File Rejections */}
      {fileRejections.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
            <h4 className="text-sm font-medium text-red-800">File Rejected</h4>
          </div>
          {fileRejections.map(({ file, errors }) => (
            <div key={file.name} className="mt-2 text-sm text-red-700">
              <p className="font-medium">{file.name}</p>
              <ul className="list-disc list-inside">
                {errors.map(error => (
                  <li key={error.code}>{error.message}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}

      {/* Upload Status */}
      {uploadStatus.type && (
        <div className={`
          border rounded-lg p-4 flex items-center
          ${uploadStatus.type === 'success' 
            ? 'bg-green-50 border-green-200' 
            : 'bg-red-50 border-red-200'
          }
        `}>
          {uploadStatus.type === 'success' ? (
            <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
          ) : (
            <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
          )}
          <p className={`text-sm font-medium ${
            uploadStatus.type === 'success' ? 'text-green-800' : 'text-red-800'
          }`}>
            {uploadStatus.message}
          </p>
        </div>
      )}
    </div>
  )
}