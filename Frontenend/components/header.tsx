'use client'

import React from 'react'
import { ThemeToggle } from './theme-toggle'

export function Header() {
  return (
    <header className="flex-none border-b border-border px-6 py-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-foreground">RAG Assistant</h1>
          <p className="text-sm text-muted-foreground mt-1">Powered by Groq Llama</p>
        </div>
        <ThemeToggle />
      </div>
    </header>
  )
}
