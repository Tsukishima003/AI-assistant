// Document Stats Component
import React from 'react';

const DocumentStats = ({ documentCount, onClearDocuments }) => {
    return (
        <div className="document-stats">
            <div className="stat-item">
                <span className="stat-label">Documents:</span>
                <span className="stat-value" id="docCount">{documentCount}</span>
            </div>
            <button
                className="clear-btn"
                id="clearBtn"
                title="Clear all documents"
                onClick={onClearDocuments}
            >
                🗑️ Clear All
            </button>
        </div>
    );
};

export default DocumentStats;
