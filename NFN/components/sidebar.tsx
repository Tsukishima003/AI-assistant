'use client'

import React, { useRef, useState } from 'react'
import { Upload, X, Wifi, WifiOff, File, Loader2 } from 'lucide-react'
import { Header } from './header'
import { api } from '@/lib/api'

interface Document {
  id: string
  name: string
  type: string
  size: number
  status: 'uploading' | 'success' | 'error'
  chunksCreated?: number
  error?: string
}

interface SidebarProps {
  documents: Document[]
  onDocumentsChange: (docs: Document[]) => void
  isConnected: boolean
}

export function Sidebar({
  documents,
  onDocumentsChange,
  isConnected,
}: SidebarProps) {
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const files = Array.from(e.dataTransfer.files)
    handleFiles(files)
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files)
      handleFiles(files)
    }
  }

  const handleFiles = async (files: File[]) => {
    const validFiles = files.filter(file => {
      const validTypes = [
        'application/pdf',
        'text/plain',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      ]
      // Also check by extension for better compatibility
      const ext = file.name.split('.').pop()?.toLowerCase()
      return validTypes.includes(file.type) || ['pdf', 'txt', 'docx'].includes(ext || '')
    })

    if (validFiles.length === 0) return

    // Create placeholder documents with uploading status
    const newDocs: Document[] = validFiles.map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      type: file.type,
      size: file.size,
      status: 'uploading' as const,
    }))

    onDocumentsChange([...documents, ...newDocs])

    // Upload each file to backend
    for (let i = 0; i < validFiles.length; i++) {
      const file = validFiles[i]
      const docId = newDocs[i].id

      try {
        const response = await api.uploadDocument(file)

        // Update document status to success
        onDocumentsChange(prevDocs =>
          prevDocs.map(doc =>
            doc.id === docId
              ? { ...doc, status: 'success' as const, chunksCreated: response.chunks_created }
              : doc
          )
        )
      } catch (error) {
        // Update document status to error
        onDocumentsChange(prevDocs =>
          prevDocs.map(doc =>
            doc.id === docId
              ? { ...doc, status: 'error' as const, error: error instanceof Error ? error.message : 'Upload failed' }
              : doc
          )
        )
      }
    }

    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const removeDocument = (id: string) => {
    onDocumentsChange(documents.filter(doc => doc.id !== id))
  }

  const clearAll = async () => {
    try {
      await api.clearDocuments()
      onDocumentsChange([])
    } catch (error) {
      console.error('Failed to clear documents:', error)
      // Still clear locally even if backend fails
      onDocumentsChange([])
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
  }

  const successfulDocs = documents.filter(d => d.status === 'success')

  return (
    <aside className="fixed left-0 top-0 h-screen w-80 flex flex-col border-r border-border bg-sidebar shadow-md">
      <Header />

      {/* Upload Zone */}
      <div className="flex-none px-6 py-6 border-b border-border">
        <div
          onClick={() => fileInputRef.current?.click()}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`scale-drag rounded-lg border-2 border-dashed p-10 text-center transition-all cursor-pointer ${isDragging
              ? 'border-primary bg-blue-50 scale-102'
              : 'border-slate-300 hover:border-primary hover:bg-slate-50'
            }`}
        >
          <Upload className="mx-auto h-8 w-8 text-muted-foreground mb-2" />
          <p className="text-sm font-medium text-foreground">Drop files here</p>
          <p className="text-xs text-muted-foreground mt-1">
            PDF, TXT, DOCX
          </p>
        </div>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.txt,.docx"
          onChange={handleFileInput}
          className="hidden"
        />
      </div>

      {/* Document List */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        <div className="flex items-center justify-between mb-4">
          <p className="text-xs font-semibold text-muted-foreground uppercase">
            Documents ({successfulDocs.length})
          </p>
          {documents.length > 0 && (
            <button
              onClick={clearAll}
              className="text-xs font-medium text-destructive hover:text-red-700 transition-colors"
            >
              Clear All
            </button>
          )}
        </div>

        <div className="space-y-2">
          {documents.length === 0 ? (
            <p className="text-sm text-muted-foreground text-center py-6">
              No documents uploaded yet
            </p>
          ) : (
            documents.map(doc => (
              <div
                key={doc.id}
                className={`flex items-start gap-3 rounded-lg bg-white p-3 border transition-colors group ${doc.status === 'error'
                    ? 'border-red-300 bg-red-50'
                    : doc.status === 'uploading'
                      ? 'border-blue-300 bg-blue-50'
                      : 'border-border hover:border-primary/50'
                  }`}
              >
                {doc.status === 'uploading' ? (
                  <Loader2 className="h-4 w-4 text-blue-500 flex-shrink-0 mt-0.5 animate-spin" />
                ) : (
                  <File className={`h-4 w-4 flex-shrink-0 mt-0.5 ${doc.status === 'error' ? 'text-red-500' : 'text-primary'
                    }`} />
                )}
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-medium text-foreground truncate">
                    {doc.name}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {doc.status === 'uploading' && 'Uploading...'}
                    {doc.status === 'error' && (doc.error || 'Upload failed')}
                    {doc.status === 'success' && (
                      doc.chunksCreated
                        ? `${formatFileSize(doc.size)} • ${doc.chunksCreated} chunks`
                        : formatFileSize(doc.size)
                    )}
                  </p>
                </div>
                {doc.status !== 'uploading' && (
                  <button
                    onClick={() => removeDocument(doc.id)}
                    className="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity"
                    aria-label="Remove document"
                  >
                    <X className="h-4 w-4 text-muted-foreground hover:text-destructive" />
                  </button>
                )}
              </div>
            ))
          )}
        </div>
      </div>

      {/* Connection Status */}
      <div className="flex-none border-t border-border px-6 py-4">
        <div className="flex items-center gap-2">
          <div className="relative">
            <div
              className={`h-2 w-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'
                } ${isConnected ? 'shadow-lg shadow-green-500/50' : ''}`}
            />
            {isConnected && (
              <div className="absolute inset-0 h-2 w-2 rounded-full bg-green-500 animate-ping" />
            )}
          </div>
          <span className="text-xs font-medium text-muted-foreground">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>
    </aside>
  )
}
