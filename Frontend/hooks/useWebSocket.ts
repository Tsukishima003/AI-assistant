'use client'

import { useState, useEffect, useRef, useCallback } from 'react'

const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'

export interface WSMessage {
    type: 'token' | 'chunk' | 'complete' | 'error' | 'info' | 'pong' | 'sources' | 'done' | 'conversation_id'
    content?: string
    sources?: string[]
}

interface UseWebSocketOptions {
    onMessage?: (message: WSMessage) => void
    onConnect?: () => void
    onDisconnect?: () => void
    onError?: (error: Event) => void
    autoReconnect?: boolean
    reconnectInterval?: number
    heartbeatInterval?: number
}

export function useWebSocket(options: UseWebSocketOptions = {}) {
    const {
        autoReconnect = true,
        reconnectInterval = 3000,
        heartbeatInterval = 30000,
    } = options

    // Refs for callbacks — always fresh, never stale
    const onMessageRef = useRef(options.onMessage)
    const onConnectRef = useRef(options.onConnect)
    const onDisconnectRef = useRef(options.onDisconnect)
    const onErrorRef = useRef(options.onError)

    useEffect(() => {
        onMessageRef.current = options.onMessage
        onConnectRef.current = options.onConnect
        onDisconnectRef.current = options.onDisconnect
        onErrorRef.current = options.onError
    })

    const [isConnected, setIsConnected] = useState(false)
    const [isConnecting, setIsConnecting] = useState(false)
    const wsRef = useRef<WebSocket | null>(null)
    const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)
    const heartbeatIntervalRef = useRef<NodeJS.Timeout | null>(null)
    const mountedRef = useRef(true)
    const isConnectingRef = useRef(false)

    const clearTimers = useCallback(() => {
        if (reconnectTimeoutRef.current) {
            clearTimeout(reconnectTimeoutRef.current)
            reconnectTimeoutRef.current = null
        }
        if (heartbeatIntervalRef.current) {
            clearInterval(heartbeatIntervalRef.current)
            heartbeatIntervalRef.current = null
        }
    }, [])

    const startHeartbeat = useCallback(() => {
        if (heartbeatIntervalRef.current) clearInterval(heartbeatIntervalRef.current)
        heartbeatIntervalRef.current = setInterval(() => {
            if (wsRef.current?.readyState === WebSocket.OPEN) {
                wsRef.current.send(JSON.stringify({ type: 'ping' }))
            }
        }, heartbeatInterval)
    }, [heartbeatInterval])

    const connect = useCallback(() => {
        if (!mountedRef.current) return
        if (wsRef.current?.readyState === WebSocket.OPEN) return
        if (isConnectingRef.current) return

        isConnectingRef.current = true
        setIsConnecting(true)
        clearTimers()

        try {
            const ws = new WebSocket(`${WS_BASE_URL}/ws/chat`)

            ws.onopen = () => {
                if (!mountedRef.current) { ws.close(); return }
                isConnectingRef.current = false
                setIsConnected(true)
                setIsConnecting(false)
                startHeartbeat()
                onConnectRef.current?.()
            }

            ws.onmessage = (event) => {
                console.log("RAW MESSAGE:",event.data)
                try {
                    const message: WSMessage = JSON.parse(event.data)
                    if (mountedRef.current) {
                        onMessageRef.current?.(message)
                    }
                } catch (e) {
                    console.error('Failed to parse WebSocket message:', e)
                }
            }

            ws.onclose = () => {
                if (!mountedRef.current) return
                isConnectingRef.current = false
                setIsConnected(false)
                setIsConnecting(false)
                clearTimers()
                onDisconnectRef.current?.()
                if (autoReconnect && mountedRef.current) {
                    reconnectTimeoutRef.current = setTimeout(() => {
                        if (mountedRef.current) connect()
                    }, reconnectInterval)
                }
            }

            ws.onerror = (error) => {
                if (!mountedRef.current) return
                isConnectingRef.current = false
                setIsConnecting(false)
                onErrorRef.current?.(error)
            }

            wsRef.current = ws
        } catch (error) {
            console.error('Failed to create WebSocket:', error)
            isConnectingRef.current = false
            setIsConnecting(false)
        }
    }, [autoReconnect, reconnectInterval, clearTimers, startHeartbeat])

    const disconnect = useCallback(() => {
        clearTimers()
        if (wsRef.current) {
            wsRef.current.close()
            wsRef.current = null
        }
        setIsConnected(false)
        setIsConnecting(false)
    }, [clearTimers])

    const sendMessage = useCallback((message: string, conversation_id?: string | null) => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({ message, conversation_id }))
            return true
        }
        return false
    }, [])

    useEffect(() => {
        mountedRef.current = true
        connect()
        return () => {
            mountedRef.current = false
            disconnect()
        }
    }, []) // eslint-disable-line react-hooks/exhaustive-deps

    return { isConnected, isConnecting, connect, disconnect, sendMessage }
}