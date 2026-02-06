'use client'

import { useState, useEffect, useRef, useCallback } from 'react'

const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'

export interface WSMessage {
    type: 'chunk' | 'sources' | 'complete' | 'error' | 'info' | 'pong'
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
        onMessage,
        onConnect,
        onDisconnect,
        onError,
        autoReconnect = true,
        reconnectInterval = 3000,
        heartbeatInterval = 30000,
    } = options

    const [isConnected, setIsConnected] = useState(false)
    const [isConnecting, setIsConnecting] = useState(false)
    const wsRef = useRef<WebSocket | null>(null)
    const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)
    const heartbeatIntervalRef = useRef<NodeJS.Timeout | null>(null)
    const mountedRef = useRef(true)

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
        if (heartbeatIntervalRef.current) {
            clearInterval(heartbeatIntervalRef.current)
        }
        heartbeatIntervalRef.current = setInterval(() => {
            if (wsRef.current?.readyState === WebSocket.OPEN) {
                wsRef.current.send(JSON.stringify({ type: 'ping' }))
            }
        }, heartbeatInterval)
    }, [heartbeatInterval])

    const connect = useCallback(() => {
        if (!mountedRef.current) return
        if (wsRef.current?.readyState === WebSocket.OPEN) return
        if (isConnecting) return

        setIsConnecting(true)
        clearTimers()

        try {
            const ws = new WebSocket(`${WS_BASE_URL}/ws/chat`)

            ws.onopen = () => {
                if (!mountedRef.current) {
                    ws.close()
                    return
                }
                setIsConnected(true)
                setIsConnecting(false)
                startHeartbeat()
                onConnect?.()
            }

            ws.onmessage = (event) => {
                console.log("recived message:" , event.data)
                console.log("mountedRef status:" , mountedRef.current)
                try {
                    const message: WSMessage = JSON.parse(event.data)
                    console.log("Parsed message:", message)
                    if (mountedRef.current && onMessage){
                        onMessage(message)
                    }
                } catch (e) {
                    console.error('Failed to parse WebSocket message:', e)
                }
            }

            ws.onclose = () => {
                if (!mountedRef.current) return
                setIsConnected(false)
                setIsConnecting(false)
                clearTimers()
                onDisconnect?.()

                if (autoReconnect && mountedRef.current) {
                    reconnectTimeoutRef.current = setTimeout(() => {
                        if (mountedRef.current) {
                            connect()
                        }
                    }, reconnectInterval)
                }
            }

            ws.onerror = (error) => {
                if (!mountedRef.current) return
                console.error('WebSocket error:', error)
                setIsConnecting(false)
                onError?.(error)
            }

            wsRef.current = ws
        } catch (error) {
            console.error('Failed to create WebSocket:', error)
            setIsConnecting(false)
        }
    }, [autoReconnect, reconnectInterval, clearTimers, startHeartbeat, onConnect, onMessage, onDisconnect, onError, isConnecting])

    const disconnect = useCallback(() => {
        clearTimers()
        if (wsRef.current) {
            wsRef.current.close()
            wsRef.current = null
        }
        setIsConnected(false)
        setIsConnecting(false)
    }, [clearTimers])

    const sendMessage = useCallback((message: string) => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({ message }))
            return true
        }
        return false
    }, [])

    // Connect on mount
    useEffect(() => {
        mountedRef.current = true
        connect()

        return () => {
            mountedRef.current = false
            disconnect()
        }
    }, []) // eslint-disable-line react-hooks/exhaustive-deps

    return {
        isConnected,
        isConnecting,
        connect,
        disconnect,
        sendMessage,
    }
}
