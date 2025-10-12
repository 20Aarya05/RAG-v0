'use client'

import { useState, useEffect } from 'react'
import { Settings, RefreshCw, CheckCircle, AlertCircle } from 'lucide-react'
import axios from 'axios'

interface EmbeddingConfig {
  provider: string
  providers: {
    [key: string]: any
  }
}

export default function ConfigPanel() {
  const [config, setConfig] = useState<EmbeddingConfig | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchConfig = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get('/api/config')
      setConfig(response.data.config)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch configuration')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchConfig()
  }, [])

  const getProviderDescription = (provider: string) => {
    switch (provider) {
      case 'dummy':
        return 'Testing provider - generates consistent dummy embeddings'
      case 'openai':
        return 'OpenAI embeddings - high quality, requires API key'
      case 'huggingface':
        return 'HuggingFace embeddings - local processing, good quality'
      default:
        return 'Unknown provider'
    }
  }

  const getProviderStatus = (provider: string) => {
    switch (provider) {
      case 'dummy':
        return { status: 'ready', message: 'Always available' }
      case 'openai':
        return { 
          status: 'warning', 
          message: 'Requires OPENAI_API_KEY environment variable' 
        }
      case 'huggingface':
        return { 
          status: 'ready', 
          message: 'Model will download automatically on first use' 
        }
      default:
        return { status: 'error', message: 'Unknown provider' }
    }
  }

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
          <span className="ml-3 text-gray-600">Loading configuration...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center py-8">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 font-medium">{error}</p>
          <button
            onClick={fetchConfig}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  if (!config) return null

  return (
    <div className="space-y-6">
      {/* Current Configuration */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <Settings className="w-5 h-5 mr-2" />
            Current Configuration
          </h3>
          <button
            onClick={fetchConfig}
            className="flex items-center px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </button>
        </div>

        <div className="space-y-4">
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium text-blue-900">Active Provider</h4>
                <p className="text-blue-700 text-sm mt-1">
                  {config.provider.charAt(0).toUpperCase() + config.provider.slice(1)}
                </p>
                <p className="text-blue-600 text-xs mt-1">
                  {getProviderDescription(config.provider)}
                </p>
              </div>
              <div className="text-right">
                {(() => {
                  const status = getProviderStatus(config.provider)
                  return (
                    <div className="flex items-center">
                      {status.status === 'ready' ? (
                        <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
                      ) : (
                        <AlertCircle className="w-5 h-5 text-yellow-500 mr-2" />
                      )}
                      <span className={`text-xs ${
                        status.status === 'ready' ? 'text-green-700' : 'text-yellow-700'
                      }`}>
                        {status.message}
                      </span>
                    </div>
                  )
                })()}
              </div>
            </div>
          </div>

          {/* Provider Settings */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(config.providers).map(([providerName, settings]) => (
              <div key={providerName} className="border border-gray-200 rounded-lg p-4">
                <h5 className="font-medium text-gray-900 mb-2">
                  {providerName.charAt(0).toUpperCase() + providerName.slice(1)} Settings
                </h5>
                <div className="space-y-2">
                  {Object.entries(settings).map(([key, value]) => (
                    <div key={key} className="flex justify-between text-sm">
                      <span className="text-gray-600">{key}:</span>
                      <span className="text-gray-900 font-mono">
                        {typeof value === 'string' ? value : JSON.stringify(value)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Configuration Instructions */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🔧 Configuration Instructions
        </h3>
        
        <div className="space-y-6">
          {/* Manual Configuration */}
          <div className="border-l-4 border-blue-500 pl-4">
            <h4 className="font-medium text-gray-900 mb-2">Manual Configuration</h4>
            <p className="text-gray-600 text-sm mb-2">
              To change embedding providers, run the configuration script:
            </p>
            <code className="block bg-gray-100 p-2 rounded text-sm font-mono">
              python configure_embeddings.py
            </code>
          </div>

          {/* Provider Options */}
          <div className="space-y-4">
            <h4 className="font-medium text-gray-900">Available Providers:</h4>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="border border-gray-200 rounded-lg p-4">
                <h5 className="font-medium text-gray-900 mb-2">🤖 Dummy</h5>
                <p className="text-sm text-gray-600 mb-2">
                  For testing and development
                </p>
                <ul className="text-xs text-gray-500 space-y-1">
                  <li>• No setup required</li>
                  <li>• Fast processing</li>
                  <li>• Consistent results</li>
                </ul>
              </div>

              <div className="border border-gray-200 rounded-lg p-4">
                <h5 className="font-medium text-gray-900 mb-2">🤗 HuggingFace</h5>
                <p className="text-sm text-gray-600 mb-2">
                  Local, high-quality embeddings
                </p>
                <ul className="text-xs text-gray-500 space-y-1">
                  <li>• No API key needed</li>
                  <li>• Good quality</li>
                  <li>• Models download once</li>
                </ul>
              </div>

              <div className="border border-gray-200 rounded-lg p-4">
                <h5 className="font-medium text-gray-900 mb-2">🚀 OpenAI</h5>
                <p className="text-sm text-gray-600 mb-2">
                  Premium quality embeddings
                </p>
                <ul className="text-xs text-gray-500 space-y-1">
                  <li>• Requires API key</li>
                  <li>• Best quality</li>
                  <li>• Usage costs apply</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Environment Variables */}
          <div className="border-l-4 border-yellow-500 pl-4">
            <h4 className="font-medium text-gray-900 mb-2">Environment Variables</h4>
            <p className="text-gray-600 text-sm mb-2">
              For OpenAI embeddings, set your API key:
            </p>
            <div className="space-y-1">
              <code className="block bg-gray-100 p-2 rounded text-sm font-mono">
                # Windows
                set OPENAI_API_KEY=your_api_key_here
              </code>
              <code className="block bg-gray-100 p-2 rounded text-sm font-mono">
                # Linux/Mac
                export OPENAI_API_KEY=your_api_key_here
              </code>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}