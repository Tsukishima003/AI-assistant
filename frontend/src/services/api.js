// API service for HTTP requests
import { API_URL } from '../config/constants';

export const uploadDocument = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData
    });

    return response.json();
};

export const getDocumentCount = async () => {
    const response = await fetch(`${API_URL}/documents/count`);
    return response.json();
};

export const clearAllDocuments = async () => {
    const response = await fetch(`${API_URL}/documents`, {
        method: 'DELETE'
    });
    return response.json();
};
