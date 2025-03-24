'use client';
import { createContext, useContext, useMemo, useEffect, useCallback } from 'react';

interface SocketContextType {
  socket: WebSocket | null;
  send: (message: string) => void;
}

const SocketContext = createContext<SocketContextType | undefined>(undefined);

export const SocketProvider = ({ children }: { children: React.ReactNode }) => {
  const socket = useMemo(() => {
    try {
      const newSocket = new WebSocket('ws://127.0.0.1:8000/ws');
      newSocket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
      return newSocket;
    } catch (error) {
      console.error('WebSocket creation error:', error);
      return null;
    }
  }, []);

  const send = useCallback((message: string) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(message);
    } else {
      console.error('WebSocket is not open or does not exist.');
    }
  }, [socket]);

  const value = useMemo(() => ({ socket, send }), [socket, send]);

  return <SocketContext.Provider value={value}>{children}</SocketContext.Provider>;
};

export const useSocket = (
  setConversationLogs: React.Dispatch<React.SetStateAction<any[]>>,
  setMessageLogs: React.Dispatch<React.SetStateAction<any[]>>,
  setConversations: React.Dispatch<React.SetStateAction<any[]>>
) => {
  const context = useContext(SocketContext);
  if (!context) {
    throw new Error('useSocket must be used within a SocketProvider');
  }

  const { socket, send } = context;

  useEffect(() => {
    if (socket) {
      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'logs_update') {
          console.log(data.chat_logs);
          console.log(data.think_logs);
          setConversationLogs(data.think_logs);
          setMessageLogs(data.chat_logs);
        }
        if (data.type === 'log_list_updates_update') {
          setConversations(data.conversation_list)
        }
      };
    }

    return () => {
      if (socket) {
        socket.onmessage = null; // Cleanup the event listener
      }
    };
  }, [socket, setConversationLogs, setMessageLogs, setConversations]);

  return { socket, send };
};

// Example usage in a component:
// import { useSocket, SocketProvider } from './SocketContext';

// const MyComponent = ({ currentConversationId }: { currentConversationId: string }) => {
//   const [conversationLogs, setConversationLogs] = useState<any[]>([]);
//   const [messageLogs, setMessageLogs] = useState<any[]>([]);
//   

//   useEffect(() => {
//     if (currentConversationId) {
//       send({ conversation_id: currentConversationId });
//     }
//   }, [currentConversationId, send]);

//   // ... rest of your component
// };