// Sidebar Component
import React from 'react';
import UploadArea from './UploadArea';
import DocumentStats from './DocumentStats';
import ConnectionStatus from './ConnectionStatus';

const Sidebar = ({
    isConnected,
    documentCount,
    isUploading,
    onUpload,
    onClearDocuments
}) => {
    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                <h1 className="logo">
                    <span className="logo-icon">🤖</span>
                    <span className="logo-text">RAG Assistant</span>
                </h1>
                <p className="subtitle">Powered by Groq Llama</p>
            </div>

            <div className="upload-section">
                <h2 className="section-title">Document Library</h2>
                <UploadArea onUpload={onUpload} isUploading={isUploading} />
                <DocumentStats
                    documentCount={documentCount}
                    onClearDocuments={onClearDocuments}
                />
            </div>

            <ConnectionStatus isConnected={isConnected} />
        </aside>
    );
};

export default Sidebar;
