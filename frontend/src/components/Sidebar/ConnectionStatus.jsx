// Connection Status Component
import React from 'react';

const ConnectionStatus = ({ isConnected }) => {
    const status = isConnected ? 'connected' : 'disconnected';
    const statusText = isConnected ? 'Connected' : 'Disconnected';

    return (
        <div className="connection-status">
            <div className={`status-indicator ${status}`} id="statusIndicator"></div>
            <span className="status-text" id="statusText">{statusText}</span>
        </div>
    );
};

export default ConnectionStatus;
