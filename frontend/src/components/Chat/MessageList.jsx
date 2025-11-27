// Message List Component
import React, { useEffect, useRef } from 'react';
import Message from './Message';
import TypingIndicator from './TypingIndicator';

const MessageList = ({ messages, isTyping }) => {
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isTyping]);

    const hasMessages = messages && messages.length > 0;

    return (
        <div className="messages-area" id="messagesArea">
            {!hasMessages && (
                <div className="welcome-message">
                    <div className="welcome-icon">✨</div>
                    <h3>Welcome to your AI Assistant!</h3>
                    <p>Upload documents to get started, then ask me anything about them.</p>
                    <div className="feature-pills">
                        <span className="pill">⚡ Real-time responses</span>
                        <span className="pill">🔍 Semantic search</span>
                        <span className="pill">📚 Source citations</span>
                    </div>
                </div>
            )}

            {hasMessages && messages.map((message, index) => (
                <Message
                    key={index}
                    content={message.content}
                    role={message.role}
                    sources={message.sources}
                />
            ))}

            {isTyping && <TypingIndicator />}
            <div ref={messagesEndRef} />
        </div>
    );
};

export default MessageList;
