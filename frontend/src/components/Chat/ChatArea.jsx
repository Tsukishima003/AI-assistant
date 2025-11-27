// Chat Area Component
import React from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

const ChatArea = ({ messages, isTyping, onSendMessage, disabled }) => {
    return (
        <main className="chat-container">
            <div className="chat-header">
                <h2>Chat with Your Documents</h2>
                <p className="chat-subtitle">Ask questions and get AI-powered answers</p>
            </div>

            <MessageList messages={messages} isTyping={isTyping} />
            <MessageInput onSendMessage={onSendMessage} disabled={disabled} />
        </main>
    );
};

export default ChatArea;
