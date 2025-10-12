'use client'

import { useState, useEffect } from 'react'
import { CheckCircle, XCircle, Clock, AlertCircle } from 'lucide-react'
import axios from 'axios'

interface ProcessingInfo {
  status: string
  filename: string
  safe_filename: string
  progress: number
  message: string
  text_file?: string
  embeddings_file?: string
}

interface ProcessingStatusProps {
  processingFiles: string[]
  onProcessingComplete: (fileId: string) => void
}

export default function ProcessingStatus({ processingFiles, onProcessingComplete }: ProcessingStatusProps) {
  const [statusData, setStatusData] = useState<Record<string, ProcessingInfo>>({})

  useEffect(() => {
    if (processingFiles.length === 0) return

    const interval = setInterval(async () => {
      const newStatusData: Record<string, ProcessingInfo> = {}

      for (const fileId of processingFiles) {
        try {
          const response = await axios.get(`/api/status/${fileId}`)
          newStatusData[fileId] = response.data.data

          // Check if processing is complete
          if (response.data.data.status === 'completed' || response.data.data.status === 'error') {
            setTimeout(() => onProcessingComplete(fileId), 2000) // Show result for 2 seconds
          }
        } catch (error) {
          console.error(`Failed to fetch status for ${fileId}:`, error)
        }
      }

      setStatusData(newStatusData)
    }, 1000) // Poll every second

    return () => clearInterval(interval)
  }, [processingFiles, onProcessingComplete])

  if (processingFiles.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <Clock className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Active Processing</h3>
        <p className="text-gray-600">
          Upload files or start processing to see status updates here
        </p>
      </div>
    )
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-6 h-6 text-green-500" />
      case 'error':
        return <XCircle className="w-6 h-6 text-red-500" />
      case 'processing':
      case 'uploaded':
        return <div className="w-6 h-6 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
      default:
        return <AlertCircle className="w-6 h-6 text-yellow-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-50 border-green-200'
      case 'error':
        return 'bg-red-50 border-red-200'
      case 'processing':
      case 'uploaded':
        return 'bg-blue-50 border-blue-200'
      default:
        return 'bg-yellow-50 border-yellow-200'
    }
  }

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          ⚡ Processing Status ({processingFiles.length} active)
        </h3>
        
        <div className="space-y-4">
          {processingFiles.map((fileId) => {
            const status = statusData[fileId]
            if (!status) {
              return (
                <div key={fileId} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center">
                    <div className="w-6 h-6 border-4 border-gray-300 border-t-transparent rounded-full animate-spin" />
                    <span className="ml-3 text-gray-600">Loading status...</span>
                  </div>
                </div>
              )
            }

            return (
              <div key={fileId} className={`border rounded-lg p-4 ${getStatusColor(status.status)}`}>
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3 flex-1">
                    {getStatusIcon(status.status)}
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-medium text-gray-900 truncate">
                        {status.filename}
                      </h4>
                      <p className="text-sm text-gray-600 mt-1">
                        {status.message}
                      </p>
                      
                      {/* Progress Bar */}
                      {status.status === 'processing' && (
                        <div className="mt-3">
                          <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                            <span>Progress</span>
                            <span>{status.progress}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${status.progress}%` }}
                            />
                          </div>
                        </div>
                      )}

                      {/* Results */}
                      {status.status === 'completed' && (
                        <div className="mt-3 space-y-1">
                          {status.text_file && (
                            <div className="text-xs text-green-700">
                              ✅ Text extracted: {status.text_file.split('/').pop()}
                            </div>
                          )}
                          {status.embeddings_file && (
                            <div className="text-xs text-green-700">
                              ✅ Embeddings created: {status.embeddings_file.split('/').pop()}
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="ml-4">
                    <span className={`
                      inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                      ${status.status === 'completed' ? 'bg-green-100 text-green-800' :
                        status.status === 'error' ? 'bg-red-100 text-red-800' :
                        status.status === 'processing' ? 'bg-blue-100 text-blue-800' :
                        'bg-yellow-100 text-yellow-800'
                      }
                    `}>
                      {status.status.charAt(0).toUpperCase() + status.status.slice(1)}
                    </span>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Processing Tips */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="text-sm font-medium text-blue-900 mb-2">💡 Processing Tips</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Large files may take several minutes to process</li>
          <li>• Text extraction happens first, then embedding generation</li>
          <li>• You can continue using the app while files process in the background</li>
          <li>• Check the Files tab to see all processed documents</li>
        </ul>
      </div>
    </div>
  )
}