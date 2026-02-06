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
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="ml-80 flex h-screen flex-col bg-background">
      {/* Messages Area */}
      {messages.length === 0 ? (
        <div className="flex-1 overflow-hidden">
          <WelcomeScreen />
        </div>
      ) : (
        <div className="flex-1 overflow-y-auto px-6 py-8">
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
            <div ref={messagesEndRef} />
          </div>
        </div>
      )}

      {/* Chat Input */}
      <ChatInput
        onSendMessage={onSendMessage}
        isDisabled={!hasDocuments}
        isLoading={isLoading}
      />
    </div>
  )
}
