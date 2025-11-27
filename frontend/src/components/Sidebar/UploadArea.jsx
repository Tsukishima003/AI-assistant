// Upload Area Component
import React, { useRef, useState } from 'react';

const UploadArea = ({ onUpload, isUploading }) => {
    const fileInputRef = useRef(null);
    const [isDragging, setIsDragging] = useState(false);

    const handleClick = () => {
        fileInputRef.current?.click();
    };

    const handleFileSelect = (e) => {
        const file = e.target.files?.[0];
        if (file) {
            onUpload(file);
            e.target.value = ''; // Reset input
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);

        const file = e.dataTransfer.files?.[0];
        if (file) {
            onUpload(file);
        }
    };

    return (
        <div
            className={`upload-area ${isDragging ? 'drag-over' : ''}`}
            onClick={handleClick}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
        >
            <input
                ref={fileInputRef}
                type="file"
                id="fileInput"
                accept=".pdf,.txt,.docx,.doc"
                hidden
                onChange={handleFileSelect}
            />
            <div className="upload-icon">{isUploading ? '⏳' : '📁'}</div>
            <p className="upload-text">
                {isUploading ? 'Uploading...' : 'Drop files here or click to browse'}
            </p>
            <p className="upload-hint">PDF, TXT, DOCX supported</p>
        </div>
    );
};

export default UploadArea;
