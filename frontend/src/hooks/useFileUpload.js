// Custom hook for file upload
import { useState, useEffect, useCallback } from 'react';
import { uploadDocument, getDocumentCount, clearAllDocuments } from '../services/api';

export const useFileUpload = (onToast) => {
    const [documentCount, setDocumentCount] = useState(0);
    const [isUploading, setIsUploading] = useState(false);

    const fetchDocumentCount = useCallback(async () => {
        try {
            const data = await getDocumentCount();
            setDocumentCount(data.count);
        } catch (error) {
            console.error('Failed to fetch document count:', error);
        }
    }, []);

    useEffect(() => {
        fetchDocumentCount();
    }, [fetchDocumentCount]);

    const handleUploadFile = useCallback(async (file) => {
        setIsUploading(true);
        onToast?.(`Uploading ${file.name}...`, 'info');

        try {
            const data = await uploadDocument(file);
            onToast?.(`✅ ${data.message}`, 'success');
            await fetchDocumentCount();
        } catch (error) {
            onToast?.(`❌ Upload error: ${error.message}`, 'error');
        } finally {
            setIsUploading(false);
        }
    }, [fetchDocumentCount, onToast]);

    const handleClearDocuments = useCallback(async () => {
        if (!confirm('Are you sure you want to clear all documents?')) {
            return;
        }

        try {
            await clearAllDocuments();
            onToast?.('All documents cleared', 'success');
            await fetchDocumentCount();
        } catch (error) {
            onToast?.(`Error: ${error.message}`, 'error');
        }
    }, [fetchDocumentCount, onToast]);

    return {
        documentCount,
        isUploading,
        uploadFile: handleUploadFile,
        clearDocuments: handleClearDocuments
    };
};
