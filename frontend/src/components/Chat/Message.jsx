// Single Message Component
import React from 'react';

const Message = ({ content, role, sources = [] }) => {
    return (
        <div className={`message ${role}`}>
            <div className="message-avatar">
                {role === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-content">
                <div className="message-bubble">
                    {content}
                </div>
                {sources && sources.length > 0 && (
                    <div className="message-sources">
                        {sources.map((source, idx) => (
                            <span key={idx} className="source-tag">
                                📄 {source.split('/').pop()}
                            </span>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Message;
