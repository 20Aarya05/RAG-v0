'use client'

import { useState, useEffect } from 'react'
import FileUpload from '@/components/FileUpload'
import FileList from '@/components/FileList'
import ProcessingStatus from '@/components/ProcessingStatus'
import ConfigPanel from '@/components/ConfigPanel'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs'
import ChatBot from '@/components/ChatBot'

export default function Home() {
  const [activeTab, setActiveTab] = useState('upload')
  const [processingFiles, setProcessingFiles] = useState<string[]>([])
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const handleFileUploaded = (fileId: string) => {
    setProcessingFiles(prev => [...prev, fileId])
    setActiveTab('status')
  }

  const handleProcessingComplete = (fileId: string) => {
    setProcessingFiles(prev => prev.filter(id => id !== fileId))
    setRefreshTrigger(prev => prev + 1)
  }

  const refreshFiles = () => {
    setRefreshTrigger(prev => prev + 1)
  }

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <div className="text-center py-8">
        <h2 className="text-4xl font-bold text-gray-900 mb-4">
          Document Processing for RAG
        </h2>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Upload your documents (PDF, DOCX, PPTX) and convert them into embeddings 
          for Retrieval-Augmented Generation. Support for both cloud and local processing.
        </p>
        <div className="mt-6">
          <button 
            onClick={() => setActiveTab('chat')}
            className="inline-flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            🤖 Try AI Assistant
          </button>
        </div>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="upload">📤 Upload</TabsTrigger>
          <TabsTrigger value="files">📁 Files</TabsTrigger>
          <TabsTrigger value="status">⚡ Status</TabsTrigger>
          <TabsTrigger value="config">⚙️ Config</TabsTrigger>
          <TabsTrigger value="chat">🤖 Chat</TabsTrigger>
        </TabsList>

        <TabsContent value="upload" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                ☁️ Cloud Upload
              </h3>
              <p className="text-gray-600 mb-4">
                Upload files through the web interface for processing
              </p>
              <FileUpload onFileUploaded={handleFileUploaded} />
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                💻 Local Processing
              </h3>
              <p className="text-gray-600 mb-4">
                Process files directly from your local Documents folder
              </p>
              <div className="space-y-3">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <h4 className="font-medium text-blue-900">Manual Processing:</h4>
                  <p className="text-blue-700 text-sm mt-1">
                    Place files in <code className="bg-blue-200 px-1 rounded">backend/RAG-embedding/Documents/</code>
                  </p>
                  <p className="text-blue-700 text-sm">
                    Run: <code className="bg-blue-200 px-1 rounded">python File_entry.py</code>
                  </p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg">
                  <h4 className="font-medium text-green-900">Batch Processing:</h4>
                  <p className="text-green-700 text-sm mt-1">
                    Process all files at once
                  </p>
                  <p className="text-green-700 text-sm">
                    Run: <code className="bg-green-200 px-1 rounded">python batch_processor.py</code>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="files">
          <FileList 
            refreshTrigger={refreshTrigger} 
            onRefresh={refreshFiles}
            onProcessFile={handleFileUploaded}
          />
        </TabsContent>

        <TabsContent value="status">
          <ProcessingStatus 
            processingFiles={processingFiles}
            onProcessingComplete={handleProcessingComplete}
          />
        </TabsContent>

        <TabsContent value="config">
          <ConfigPanel />
        </TabsContent>

        <TabsContent value="chat">
          <ChatBot />
        </TabsContent>
      </Tabs>
    </div>
  )
}