// Typing Indicator Component
import React from 'react';

const TypingIndicator = () => {
    return (
        <div className="message assistant typing-message">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
                <div className="message-bubble typing-indicator">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                </div>
            </div>
        </div>
    );
};

export default TypingIndicator;
