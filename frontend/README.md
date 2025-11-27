# RAG Chat Application - React Frontend

A modern, real-time chat application powered by RAG (Retrieval-Augmented Generation) built with **React** and **Vite**.

## 🚀 Quick Start

### Prerequisites

- Node.js (v14 or higher)
- Backend server running on `http://localhost:8000`

### Installation & Running

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will automatically open at **http://localhost:3000** 🎉

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Chat/
│   │   │   ├── ChatArea.jsx        # Main chat container
│   │   │   ├── MessageList.jsx     # Messages display
│   │   │   ├── Message.jsx         # Individual message
│   │   │   ├── MessageInput.jsx    # Input field
│   │   │   └── TypingIndicator.jsx # Typing animation
│   │   ├── Sidebar/
│   │   │   ├── Sidebar.jsx         # Sidebar container
│   │   │   ├── UploadArea.jsx      # File upload
│   │   │   ├── DocumentStats.jsx   # Document count
│   │   │   └── ConnectionStatus.jsx # Connection indicator
│   │   └── Toast.jsx               # Toast notifications
│   ├── hooks/
│   │   ├── useWebSocket.js         # WebSocket hook
│   │   ├── useFileUpload.js        # File upload hook
│   │   └── useToast.js             # Toast hook
│   ├── services/
│   │   └── api.js                  # API calls
│   ├── config/
│   │   └── constants.js            # Configuration
│   ├── App.jsx                     # Main App component
│   ├── App.css                     # Application styles
│   ├── main.jsx                    # Entry point
│   └── index.css                   # Base styles
├── public/                         # Static assets
├── index.html                      # HTML template
├── vite.config.js                  # Vite configuration
└── package.json                    # Dependencies
```

## ✨ Features

- **React Components**: Modular, reusable UI components
- **Custom Hooks**: Clean state management with React hooks
- **Real-time Chat**: WebSocket-based instant messaging
- **Document Upload**: Drag & drop PDF, TXT, DOCX files
- **Streaming Responses**: Token-by-token AI response streaming
- **Source Citations**: See which documents were used for answers
- **Auto-reconnect**: Automatic WebSocket reconnection
- **Hot Module Replacement**: Instant updates during development
- **Modern UI**: Clean, responsive interface

## 🛠️ Development

### Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server on port 3000 with HMR |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

### Making Changes

The development server features Hot Module Replacement (HMR) - changes are reflected instantly:
- Edit React components in `src/components/`
- Modify hooks in `src/hooks/`
- Update styles in `src/App.css`
- Configure in `src/config/constants.js`

## 🏗️ Architecture

### Component Hierarchy

```
App
├── Sidebar
│   ├── UploadArea
│   ├── DocumentStats
│   └── ConnectionStatus
├── ChatArea
│   ├── MessageList
│   │   ├── Message (multiple)
│   │   └── TypingIndicator
│   └── MessageInput
└── Toast
```

### Custom Hooks

- **useWebSocket**: Manages WebSocket connection, message handling, and state
- **useFileUpload**: Handles file uploads and document management
- **useToast**: Manages toast notifications

### State Management

Uses React hooks for state management:
- WebSocket state in `useWebSocket`
- Upload state in `useFileUpload`
- UI state in individual components

## 🔧 Configuration

Edit `src/config/constants.js` to change API endpoints:

```javascript
export const API_URL = 'http://localhost:8000';
export const WS_URL = 'ws://localhost:8000/ws/chat';
```

## 🧪 Testing

1. Start the backend server
2. Run `npm run dev`
3. Verify:
   - ✅ Connection status shows "Connected"
   - ✅ File upload works (drag & drop)
   - ✅ Messages send and receive
   - ✅ Streaming responses display
   - ✅ Source citations appear
   - ✅ HMR updates work

## 📚 Tech Stack

- **React 18** - UI library
- **Vite** - Build tool & dev server
- **WebSocket API** - Real-time communication
- **Fetch API** - HTTP requests
- **CSS3** - Styling

## 🤝 Contributing

1. Follow React best practices
2. Use functional components with hooks
3. Keep components small and focused
4. Add JSDoc comments for exported functions
5. Test your changes before committing

## 📝 License

ISC

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found errors | Run `npm install` |
| Connection failed | Ensure backend is running on port 8000 |
| Page won't load | Check browser console for errors |
| Changes not reflecting | Check if HMR is working, try hard refresh (Ctrl+F5) |
| Build errors | Delete `node_modules` and run `npm install` again |

---

**Built with React + Vite for a modern, fast development experience** ⚡
