const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface UploadResponse {
  filename: string
  status: string
  chunks_created: number
  message: string
}

export interface ChatResponse {
  response: string
  sources: string[]
  conversation_id: string
}

export interface DocumentCountResponse {
  count: number
}

export const api = {
  /**
   * Upload a document to be processed and indexed
   */
  async uploadDocument(file: File): Promise<UploadResponse> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Upload failed' }))
      throw new Error(error.detail || 'Upload failed')
    }

    return response.json()
  },

  /**
   * Send a chat message (non-streaming fallback)
   */
  async chat(message: string, conversationId?: string): Promise<ChatResponse> {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      }),
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Chat request failed' }))
      throw new Error(error.detail || 'Chat request failed')
    }

    return response.json()
  },

  /**
   * Get the count of indexed documents
   */
  async getDocumentCount(): Promise<DocumentCountResponse> {
    const response = await fetch(`${API_BASE_URL}/documents/count`)

    if (!response.ok) {
      throw new Error('Failed to get document count')
    }

    return response.json()
  },

  /**
   * Clear all documents from the vector store
   */
  async clearDocuments(): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/documents`, {
      method: 'DELETE',
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to clear documents' }))
      throw new Error(error.detail || 'Failed to clear documents')
    }
  },

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string; documents_indexed: number; model: string }> {
    const response = await fetch(`${API_BASE_URL}/health`)

    if (!response.ok) {
      throw new Error('Backend is not available')
    }

    return response.json()
  },
}
