'use client'

import React from 'react'
import { Loader2 } from 'lucide-react'

interface ChatMessageProps {
  role: 'user' | 'assistant'
  content: string
  isLoading?: boolean
  sources?: string[]
}

export function ChatMessage({
  role,
  content,
  isLoading,
  sources,
}: ChatMessageProps) {
  const isAssistant = role === 'assistant'

  return (
    <div className={`flex gap-4 ${isAssistant ? 'justify-start' : 'justify-end'}`}>
      <div
        className={`max-w-xl rounded-lg px-4 py-3 ${
          isAssistant
            ? 'bg-card border border-border text-foreground'
            : 'bg-primary text-primary-foreground'
        }`}
      >
        <div className="flex items-center gap-2">
          {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
          <p className="text-sm">{content}</p>
        </div>

        {/* Source Citations */}
        {isAssistant && sources && sources.length > 0 && (
          <div className="mt-3 pt-3 border-t border-border">
            <p className="text-xs font-medium text-muted-foreground mb-2">
              Sources:
            </p>
            <div className="space-y-1">
              {sources.map((source, idx) => (
                <p key={idx} className="text-xs text-muted-foreground">
                  • {source}
                </p>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
