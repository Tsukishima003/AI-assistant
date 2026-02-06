'use client'

import React from 'react'
import { Zap, Search, BookOpen } from 'lucide-react'

export function WelcomeScreen() {
  const features = [
    {
      icon: Zap,
      label: 'Real-time responses',
      description: 'Get instant AI-powered answers',
    },
    {
      icon: Search,
      label: 'Semantic search',
      description: 'Intelligent document retrieval',
    },
    {
      icon: BookOpen,
      label: 'Source citations',
      description: 'Know where information comes from',
    },
  ]

  return (
    <div className="fade-in flex h-full flex-col items-center justify-center px-6 py-12 text-center">
      <div className="max-w-2xl">
        <h2 className="text-balance text-4xl font-semibold text-foreground mb-4">
          Chat with Your Documents
        </h2>
        <p className="text-xl text-muted-foreground mb-12">
          Ask questions and get AI-powered answers
        </p>

        {/* Welcome Message */}
        <div className="mb-12 rounded-lg bg-gradient-to-r from-blue-50 to-purple-50 border border-primary/20 p-6">
          <p className="text-lg text-foreground">
            Welcome to your AI Assistant!
          </p>
          <p className="text-sm text-muted-foreground mt-2">
            Upload documents from the sidebar to get started, then ask any
            questions about their content.
          </p>
        </div>

        {/* Feature Badges */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          {features.map(feature => {
            const Icon = feature.icon
            return (
              <div
                key={feature.label}
                className="rounded-full border border-primary/20 bg-blue-50/50 px-4 py-3 backdrop-blur-sm hover:border-primary/40 hover:bg-blue-50/80 transition-all"
              >
                <div className="flex items-center justify-center gap-2 mb-2">
                  <Icon className="h-5 w-5 text-primary" />
                  <p className="text-sm font-medium text-foreground">
                    {feature.label}
                  </p>
                </div>
                <p className="text-xs text-muted-foreground">
                  {feature.description}
                </p>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
