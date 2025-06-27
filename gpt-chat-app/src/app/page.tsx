'use client';

import { useEffect, useState, useCallback } from 'react';
import { useTheme } from '@/utils/hooks/useTheme';
import SidebarHeader from '@/components/Sidebar/SidebarHeader';
import ConversationList from '@/components/Sidebar/ConversationList';
import ThinkContainer from '@/components/ThinkLogs/ThinkContainer';
import ChatContainer from '@/components/Chat/ChatContainer';
import ChatInput from '@/components/Chat/ChatInput';
import ThemeToggle from '@/components/ui/ThemeToggle';
import { getConversations, createConversation } from '@/utils/api/conversations';
import type { Conversation } from '@/types';
import type { LogEntry } from '@/types';
import type { Message } from '@/types';
import { useSocket } from "@/utils/context/socket";

export default function Home() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [conversationLogs, setConversationLogs] = useState<LogEntry[]>([]);
  const [messageLogs, setMessageLogs] = useState<Message[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [isThinking, setIsThinking] = useState(false);
  const { theme, toggleTheme } = useTheme();
  const { send, isConnected } = useSocket(setConversationLogs, setMessageLogs, setConversations);

  // 使用 useCallback 來穩定 handleNewConversation 函數
  const handleNewConversation = useCallback(async () => {
    try {
      const data = await createConversation();
      setCurrentConversationId(data.conversation_id);
    } catch (error) {
      console.error('Error creating new conversation:', error);
    }
  }, []);

  // 初始化對話列表
  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const data = await getConversations();
        setConversations(data);
        if (data.length > 0 && !currentConversationId) {
          setCurrentConversationId(data[0].id);
        } else if (data.length === 0) {
          handleNewConversation();
        }
      } catch (error) {
        console.error('Error fetching conversations:', error);
      }
    };

    fetchConversations();
  }, [handleNewConversation]);

  const handleStartNewConversation = () => {
    send(JSON.stringify({ type: "start_conversation", content: {} }));
  };

  const handleConversationSelect = (id: string) => {
    setCurrentConversationId(id);
  };

  const handleSendMessage = async (user_input: string) => {
    if (!user_input.trim() || !currentConversationId) return;
    
    setIsThinking(true);
    send(JSON.stringify({ type: "user_input", content: { message: user_input } }));
    
    try {
      // Message sending logic will be implemented in the ChatInput component
      // This is just to control the thinking indicator
      setTimeout(() => {
        setIsThinking(false);
      }, 2000);
    } catch (error) {
      console.error('Error sending message:', error);
      setIsThinking(false);
    }
  };

  // 當對話 ID 或連線狀態改變時，獲取對話內容
  const switchConversation = useCallback((conversationId: string) => {
    if (isConnected) {
      send(JSON.stringify({ type: "get_conversation", content: { conversation_id: conversationId } }));
    }
  }, [send, isConnected]);

  useEffect(() => {
    if (!currentConversationId || !isConnected) return;
    switchConversation(currentConversationId);
  }, [currentConversationId, switchConversation, isConnected]);

  return (
    <div className={`flex flex-col h-screen ${theme === 'dark' ? 'dark' : ''}`}>
      <header className="bg-gray-100 text-gray-800 p-4 text-center shadow-md">
        <h1 className="text-2xl font-bold">Chat Interface</h1>
      </header>
      
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <div className="w-1/5 bg-gray-200 text-gray-800 flex flex-col border-r border-gray-300">
          <div className="flex-1 overflow-y-auto p-4">
            <ConversationList 
              conversations={conversations} 
              currentId={currentConversationId} 
              onSelect={handleConversationSelect} 
            />
          </div>
          <div className="p-3 border-t border-gray-300 flex justify-center">
            <button 
              onClick={handleStartNewConversation}
              className="bg-white text-gray-800 hover:bg-gray-100 rounded-full w-10 h-10 flex items-center justify-center shadow-md"
              aria-label="Start new conversation"
            >
              <span className="text-xl font-bold">+</span>
            </button>
          </div>
        </div>
        
        {/* Think Logs */}
        <div className="flex-1 bg-white flex flex-col border-r border-gray-300">
          <div className="p-4 border-b border-white flex justify-between items-center">
            <h2 className="text-lg font-medium text-gray-800">Thinking Process</h2>
            {isThinking && <div className="thinking-indicator"></div>}
          </div>
          <ThinkContainer conversationLogs={conversationLogs} isThinking={isThinking} />
        </div>
        
        {/* Chat */}
        <div className="flex-1 bg-white flex flex-col">
          <div className="p-4 border-b border-white flex justify-between items-center">
            <h2 className="text-lg font-medium text-gray-800">Chat</h2>
          </div>
          <ChatContainer messageLogs={messageLogs} />
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
      </div>
      
      <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
    </div>
  );
}