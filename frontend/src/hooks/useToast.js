// Custom hook for toast notifications
import { useState, useCallback } from 'react';

export const useToast = () => {
    const [toast, setToast] = useState({ message: '', type: '', show: false });

    const showToast = useCallback((message, type = 'info') => {
        setToast({ message, type, show: true });

        setTimeout(() => {
            setToast(prev => ({ ...prev, show: false }));
        }, 3000);
    }, []);

    return {
        toast,
        showToast
    };
};
