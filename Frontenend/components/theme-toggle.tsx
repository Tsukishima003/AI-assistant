'use client'

import React, { useEffect, useState, useContext } from 'react'
import { Moon, Sun } from 'lucide-react'
import { ThemeContext } from './theme-provider'

export function ThemeToggle() {
  const [mounted, setMounted] = useState(false)
  const context = useContext(ThemeContext)

  // Ensure component only renders on client after hydration
  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted || !context) {
    return (
      <button
        className="flex-shrink-0 rounded-lg p-2 hover:bg-muted transition-colors"
        aria-label="Toggle theme"
        disabled
      >
        <div className="h-5 w-5 bg-muted rounded" />
      </button>
    )
  }

  const { theme, toggleTheme } = context

  return (
    <button
      onClick={toggleTheme}
      className="flex-shrink-0 rounded-lg p-2 hover:bg-muted transition-colors"
      aria-label="Toggle theme"
      title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
    >
      {theme === 'light' ? (
        <Moon className="h-5 w-5 text-muted-foreground hover:text-foreground" />
      ) : (
        <Sun className="h-5 w-5 text-muted-foreground hover:text-foreground" />
      )}
    </button>
  )
}
