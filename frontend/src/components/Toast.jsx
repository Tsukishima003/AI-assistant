// Toast Component
import React from 'react';

const Toast = ({ toast }) => {
    return (
        <div className={`toast ${toast.type} ${toast.show ? 'show' : ''}`} id="toast">
            {toast.message}
        </div>
    );
};

export default Toast;
