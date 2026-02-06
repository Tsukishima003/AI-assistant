'use client'

import React, { useState, useRef, useEffect } from 'react'
import { Send } from 'lucide-react'

interface ChatInputProps {
  onSendMessage: (message: string) => void
  isDisabled?: boolean
  isLoading?: boolean
}

export function ChatInput({
  onSendMessage,
  isDisabled,
  isLoading,
}: ChatInputProps) {
  const [input, setInput] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(
        textareaRef.current.scrollHeight,
        120
      ) + 'px'
    }
  }, [input])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !isDisabled && !isLoading) {
      onSendMessage(input.trim())
      setInput('')
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
      }
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex-none border-t border-border bg-background p-6">
      <div className="mx-auto max-w-2xl flex gap-3">
        <div className="relative flex-1">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSubmit(e)
              }
            }}
            placeholder="Ask a question about your documents..."
            disabled={isDisabled || isLoading}
            className="w-full resize-none rounded-lg border border-border bg-white px-4 py-3 text-sm text-foreground placeholder-muted-foreground transition-all focus:outline-none focus:border-primary focus:ring-3 focus:ring-primary/10 disabled:opacity-50 disabled:cursor-not-allowed"
            rows={1}
          />
        </div>
        <button
          type="submit"
          disabled={isDisabled || !input.trim() || isLoading}
          className="flex-shrink-0 rounded-lg bg-primary px-4 py-3 text-primary-foreground transition-all hover:opacity-90 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          aria-label="Send message"
        >
          <Send className="h-5 w-5" />
        </button>
      </div>
    </form>
  )
}
