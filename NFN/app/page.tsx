'use client'

import React, { useState, useCallback, useRef } from 'react'
import { Sidebar } from '@/components/sidebar'
import { ChatArea } from '@/components/chat-area'
import { useWebSocket, WSMessage } from '@/hooks/useWebSocket'

interface Document {
  id: string
  name: string
  type: string
  size: number
  status: 'uploading' | 'success' | 'error'
  chunksCreated?: number
  error?: string
}

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
  isLoading?: boolean
}

export default function Home() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const currentMessageRef = useRef<string>('')
  const currentSourcesRef = useRef<string[]>([])

  const handleWSMessage = useCallback((message: WSMessage) => {
    console.log('🎯 Handling message type:', message.type)
    
    switch (message.type) {
      case 'token':
      case 'chunk':
        currentMessageRef.current += message.content || ''
        setMessages(prev => {
          const updated = [...prev]
          const lastMessage = updated[updated.length - 1]
          if (lastMessage?.role === 'assistant' && lastMessage.isLoading) {
            // Create a NEW object instead of mutating
            updated[updated.length - 1] = {
              ...lastMessage,
              content: currentMessageRef.current
            }
          }
          return updated
        })
        break

      case 'sources':
        currentSourcesRef.current = message.sources || []
        break

      case 'done':
      case 'complete':
        setMessages(prev => {
          const updated = [...prev]
          const lastMessage = updated[updated.length - 1]
          if (lastMessage?.role === 'assistant') {
            // Create a NEW object
            updated[updated.length - 1] = {
              ...lastMessage,
              isLoading: false,
              sources: currentSourcesRef.current.length > 0
                ? currentSourcesRef.current
                : undefined
            }
          }
          return updated
        })
        setIsLoading(false)
        currentMessageRef.current = ''
        currentSourcesRef.current = []
        break

      case 'error':
        setMessages(prev => {
          const updated = [...prev]
          const lastMessage = updated[updated.length - 1]
          if (lastMessage?.role === 'assistant' && lastMessage.isLoading) {
            // Create a NEW object
            updated[updated.length - 1] = {
              ...lastMessage,
              content: `Error: ${message.content || 'Something went wrong'}`,
              isLoading: false
            }
          }
          return updated
        })
        setIsLoading(false)
        currentMessageRef.current = ''
        currentSourcesRef.current = []
        break

      case 'info':
        setMessages(prev => {
          const updated = [...prev]
          const lastMessage = updated[updated.length - 1]
          if (lastMessage?.role === 'assistant' && lastMessage.isLoading) {
            // Create a NEW object
            updated[updated.length - 1] = {
              ...lastMessage,
              content: message.content || '',
              isLoading: false
            }
          }
          return updated
        })
        setIsLoading(false)
        currentMessageRef.current = ''
        break

      case 'pong':
        break
        
      default:
        console.warn('Unknown message type:', message.type)
    }
  }, [])



  const { isConnected, sendMessage: wsSendMessage } = useWebSocket({
    onMessage: handleWSMessage,
    onConnect: () => console.log('WebSocket connected'),
    onDisconnect: () => console.log('WebSocket disconnected'),
  })

  const handleDocumentsChange = useCallback((newDocs: Document[]) => {
    setDocuments(newDocs)
  }, [])

  const handleSendMessage = useCallback(async (content: string) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
    }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    // Reset refs for new message
    currentMessageRef.current = ''
    currentSourcesRef.current = []

    // Add placeholder assistant message
    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: '',
      isLoading: true,
    }
    setMessages(prev => [...prev, assistantMessage])

    // Send via WebSocket
    const sent = wsSendMessage(content)
    if (!sent) {
      // WebSocket not connected, update message with error
      setMessages(prev => {
        const updated = [...prev]
        const lastMessage = updated[updated.length - 1]
        if (lastMessage?.role === 'assistant' && lastMessage.isLoading) {
          lastMessage.content = 'Unable to send message. Please check your connection.'
          lastMessage.isLoading = false
        }
        return updated
      })
      setIsLoading(false)
    }
  }, [wsSendMessage])

  const successfulDocs = documents.filter(d => d.status === 'success')

  return (
    <main className="h-screen w-screen overflow-hidden bg-background">
      <Sidebar
        documents={documents}
        onDocumentsChange={handleDocumentsChange}
        isConnected={isConnected}
      />
      <ChatArea
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        hasDocuments={successfulDocs.length > 0}
      />
    </main>
  )
}
