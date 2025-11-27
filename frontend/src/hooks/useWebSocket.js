// Custom hook for WebSocket connection
import { useState, useEffect, useCallback, useRef } from 'react';
import { WS_URL } from '../config/constants';

export const useWebSocket = () => {
    const [isConnected, setIsConnected] = useState(false);
    const [messages, setMessages] = useState([]);
    const [isTyping, setIsTyping] = useState(false);
    const wsRef = useRef(null);
    const currentMessageRef = useRef('');

    useEffect(() => {
        const connectWebSocket = () => {
            const ws = new WebSocket(WS_URL);
            wsRef.current = ws;

            ws.onopen = () => {
                console.log('WebSocket opened');
                setIsConnected(true);
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                handleMessage(data);
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            ws.onclose = () => {
                console.log('WebSocket closed');
                setIsConnected(false);

                // Attempt to reconnect after 1 second
                setTimeout(() => {
                    if (!wsRef.current || wsRef.current.readyState === WebSocket.CLOSED) {
                        console.log('Attempting to reconnect...');
                        connectWebSocket();
                    }
                }, 1000);
            };
        };

        const handleMessage = (data) => {
            const { type, content } = data;

            switch (type) {
                case 'token':
                    // Append token to current message
                    currentMessageRef.current += content;
                    setMessages(prev => {
                        const newMessages = [...prev];
                        const lastMessage = newMessages[newMessages.length - 1];

                        if (lastMessage && lastMessage.role === 'assistant' && !lastMessage.isComplete) {
                            lastMessage.content = currentMessageRef.current;
                            return newMessages;
                        } else {
                            return [...prev, { role: 'assistant', content, sources: [], isComplete: false }];
                        }
                    });
                    break;

                case 'sources':
                    // Add sources to last message
                    setMessages(prev => {
                        const newMessages = [...prev];
                        const lastMessage = newMessages[newMessages.length - 1];
                        if (lastMessage) {
                            lastMessage.sources = content;
                        }
                        return newMessages;
                    });
                    break;

                case 'done':
                    // Mark message as complete
                    currentMessageRef.current = '';
                    setMessages(prev => {
                        const newMessages = [...prev];
                        const lastMessage = newMessages[newMessages.length - 1];
                        if (lastMessage) {
                            lastMessage.isComplete = true;
                        }
                        return newMessages;
                    });
                    setIsTyping(false);
                    break;

                case 'error':
                    console.error('Error from server:', content);
                    setIsTyping(false);
                    break;

                case 'info':
                    console.log('Info from server:', content);
                    setIsTyping(false);
                    break;

                default:
                    console.warn('Unknown message type:', type);
            }
        };

        connectWebSocket();

        return () => {
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, []);

    const sendMessage = useCallback((message) => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            // Add user message to messages
            setMessages(prev => [...prev, { role: 'user', content: message, sources: [], isComplete: true }]);

            // Show typing indicator
            setIsTyping(true);
            currentMessageRef.current = '';

            // Send message via WebSocket
            wsRef.current.send(JSON.stringify({ message }));

            return true;
        }
        return false;
    }, []);

    return {
        isConnected,
        messages,
        isTyping,
        sendMessage
    };
};
