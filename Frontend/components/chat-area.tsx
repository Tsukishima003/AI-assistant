'use client'

import React, { useRef, useEffect } from 'react'
import { ChatMessage } from './chat-message'
import { ChatInput } from './chat-input'
import { WelcomeScreen } from './welcome-screen'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
  isLoading?: boolean
}

interface ChatAreaProps {
  messages: Message[]
  onSendMessage: (message: string) => void
  isLoading?: boolean
  hasDocuments: boolean
}

export function ChatArea({
  messages,
  onSendMessage,
  isLoading,
  hasDocuments,
}: ChatAreaProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTo({
        top: containerRef.current.scrollHeight,
        behavior: 'smooth',
      })
    }
  }, [messages])

  return (
    <div className="ml-80 flex h-screen flex-col bg-background">
      {messages.length === 0 ? (
        <div className="flex-1 overflow-hidden">
          <WelcomeScreen />
        </div>
      ) : (
        <div
          ref={containerRef}
          className="flex-1 overflow-y-auto px-6 py-8 min-h-0"
        >
          <div className="mx-auto max-w-2xl space-y-6">
            {messages.map(message => (
              <ChatMessage
                key={message.id}
                role={message.role}
                content={message.content}
                isLoading={message.isLoading}
                sources={message.sources}
              />
            ))}
          </div>
        </div>
      )}

      <div className="shrink-0">
        <ChatInput
          onSendMessage={onSendMessage}
          isDisabled={!hasDocuments}
          isLoading={isLoading}
        />
      </div>
    </div>
  )
}