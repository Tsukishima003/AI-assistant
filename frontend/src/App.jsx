// Main App Component
import React from 'react';
import Sidebar from './components/Sidebar/Sidebar';
import ChatArea from './components/Chat/ChatArea';
import Toast from './components/Toast';
import { useWebSocket } from './hooks/useWebSocket';
import { useFileUpload } from './hooks/useFileUpload';
import { useToast } from './hooks/useToast';
import './App.css';

function App() {
  const { isConnected, messages, isTyping, sendMessage } = useWebSocket();
  const { toast, showToast } = useToast();
  const { documentCount, isUploading, uploadFile, clearDocuments } = useFileUpload(showToast);

  const handleSendMessage = (message) => {
    const success = sendMessage(message);
    if (!success) {
      showToast('Not connected to server', 'error');
    }
  };

  return (
    <div className="app-container">
      <Sidebar
        isConnected={isConnected}
        documentCount={documentCount}
        isUploading={isUploading}
        onUpload={uploadFile}
        onClearDocuments={clearDocuments}
      />
      <ChatArea
        messages={messages}
        isTyping={isTyping}
        onSendMessage={handleSendMessage}
        disabled={!isConnected || isTyping}
      />
      <Toast toast={toast} />
    </div>
  );
}

export default App;
