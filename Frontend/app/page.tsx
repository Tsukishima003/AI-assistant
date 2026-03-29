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
  status: 'uploading' | 'processing' | 'success' | 'error'
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
  const assistantMessageIdRef = useRef<string>('')

  const handleWSMessage = useCallback((message: WSMessage) => {
    switch (message.type) {
      case 'token':
      case 'chunk':
        currentMessageRef.current += message.content || ''
        setMessages(prev =>
          prev.map(msg =>
            msg.id === assistantMessageIdRef.current
              ? { ...msg, content: currentMessageRef.current, isLoading: true }
              : msg
          )
        )
        break

      case 'sources':
        currentSourcesRef.current = message.sources || []
        break

      case 'done':
      case 'complete':
        setMessages(prev =>
          prev.map(msg =>
            msg.id === assistantMessageIdRef.current
              ? {
                  ...msg,
                  content: currentMessageRef.current || message.content || msg.content,
                  isLoading: false,
                  sources: currentSourcesRef.current.length > 0
                    ? currentSourcesRef.current
                    : undefined,
                }
              : msg
          )
        )
        setIsLoading(false)
        currentMessageRef.current = ''
        currentSourcesRef.current = []
        assistantMessageIdRef.current = ''
        break

      case 'error':
        setMessages(prev =>
          prev.map(msg =>
            msg.id === assistantMessageIdRef.current
              ? {
                  ...msg,
                  content: `Error: ${message.content || 'Something went wrong'}`,
                  isLoading: false,
                }
              : msg
          )
        )
        setIsLoading(false)
        currentMessageRef.current = ''
        currentSourcesRef.current = []
        assistantMessageIdRef.current = ''
        break

      case 'info':
        setMessages(prev =>
          prev.map(msg =>
            msg.id === assistantMessageIdRef.current
              ? { ...msg, content: message.content || '', isLoading: false }
              : msg
          )
        )
        setIsLoading(false)
        currentMessageRef.current = ''
        assistantMessageIdRef.current = ''
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

  const handleDocumentsChange = useCallback(
    (newDocs: Document[] | ((prev: Document[]) => Document[])) => {
      setDocuments(newDocs as any)
    }, []
  )

  const handleSendMessage = useCallback(async (content: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content,
    }

    const assistantId = crypto.randomUUID()
    assistantMessageIdRef.current = assistantId

    const assistantMessage: Message = {
      id: assistantId,
      role: 'assistant',
      content: '',
      isLoading: true,
    }

    setMessages(prev => [...prev, userMessage, assistantMessage])
    setIsLoading(true)
    currentMessageRef.current = ''
    currentSourcesRef.current = []

    const sent = wsSendMessage(content)
    if (!sent) {
      setMessages(prev =>
        prev.map(msg =>
          msg.id === assistantId
            ? {
                ...msg,
                content: 'Unable to send message. Check your connection....',
                isLoading: false,
              }
            : msg
        )
      )
      setIsLoading(false)
      assistantMessageIdRef.current = ''
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