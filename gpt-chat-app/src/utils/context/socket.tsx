'use client';
import { createContext, useContext, useEffect, useCallback, useState } from 'react';
import type { LogEntry, Message, Conversation } from '@/types';

interface SocketContextType {
  send: (message: string) => void;
  isConnected: boolean;
}

const SocketContext = createContext<SocketContextType | undefined>(undefined);

// 模組級別的 WebSocket 單例
let globalSocket: WebSocket | null = null;
let connectionPromise: Promise<WebSocket> | null = null;

// 創建 WebSocket 連線的函數
const createWebSocket = (): Promise<WebSocket> => {
  if (connectionPromise) {
    return connectionPromise;
  }

  connectionPromise = new Promise((resolve, reject) => {
    try {
      const socket = new WebSocket('ws://127.0.0.1:8000/ws');
      
      socket.onopen = () => {
        console.log('WebSocket connected');
        globalSocket = socket;
        resolve(socket);
      };

      socket.onclose = () => {
        console.log('WebSocket disconnected');
        globalSocket = null;
        connectionPromise = null;
      };

      socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        globalSocket = null;
        connectionPromise = null;
        reject(error);
      };
    } catch (error) {
      console.error('WebSocket creation error:', error);
      connectionPromise = null;
      reject(error);
    }
  });

  return connectionPromise;
};

// 獲取 WebSocket 實例的函數
const getWebSocket = async (): Promise<WebSocket> => {
  if (globalSocket && globalSocket.readyState === WebSocket.OPEN) {
    return globalSocket;
  }
  return createWebSocket();
};

export const SocketProvider = ({ children }: { children: React.ReactNode }) => {
  const [isConnected, setIsConnected] = useState(false);

  // 初始化 WebSocket 連線
  useEffect(() => {
    let mounted = true;

    const initSocket = async () => {
      try {
        await getWebSocket();
        if (mounted) {
          setIsConnected(true);
        }
      } catch (error) {
        console.error('Failed to initialize WebSocket:', error);
        if (mounted) {
          setIsConnected(false);
        }
      }
    };

    initSocket();

    return () => {
      mounted = false;
    };
  }, []);

  const send = useCallback(async (message: string) => {
    try {
      const socket = await getWebSocket();
      if (socket.readyState === WebSocket.OPEN) {
        socket.send(message);
      } else {
        console.error('WebSocket is not open');
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  }, []);

  const value = { send, isConnected };

  return <SocketContext.Provider value={value}>{children}</SocketContext.Provider>;
};

export const useSocket = (
  setConversationLogs: React.Dispatch<React.SetStateAction<LogEntry[]>>,
  setMessageLogs: React.Dispatch<React.SetStateAction<Message[]>>,
  setConversations: React.Dispatch<React.SetStateAction<Conversation[]>>
) => {
  const context = useContext(SocketContext);
  if (!context) {
    throw new Error('useSocket must be used within a SocketProvider');
  }

  const { send, isConnected } = context;

  // 使用 useCallback 來穩定 setter 函數的引用
  const stableSetConversationLogs = useCallback(setConversationLogs, []);
  const stableSetMessageLogs = useCallback(setMessageLogs, []);
  const stableSetConversations = useCallback(setConversations, []);

  useEffect(() => {
    let mounted = true;

    const setupMessageHandler = async () => {
      try {
        const socket = await getWebSocket();
        
        const handleMessage = (event: MessageEvent) => {
          if (!mounted) return;
          
          try {
            const data = JSON.parse(event.data);
            if (data.type === 'logs_update') {
              console.log(data.chat_logs);
              console.log(data.think_logs);
              stableSetConversationLogs(data.think_logs);
              stableSetMessageLogs(data.chat_logs);
            }
            if (data.type === 'log_list_updates_update') {
              stableSetConversations(data.conversation_list)
            }
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        socket.addEventListener('message', handleMessage);

        return () => {
          socket.removeEventListener('message', handleMessage);
        };
      } catch (error) {
        console.error('Failed to setup message handler:', error);
      }
    };

    if (isConnected) {
      setupMessageHandler();
    }

    return () => {
      mounted = false;
    };
  }, [isConnected, stableSetConversationLogs, stableSetMessageLogs, stableSetConversations]);

  return { send, isConnected };
};

// 清理函數，用於應用關閉時清理連線
export const cleanupWebSocket = () => {
  if (globalSocket) {
    globalSocket.close();
    globalSocket = null;
  }
  connectionPromise = null;
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
// };