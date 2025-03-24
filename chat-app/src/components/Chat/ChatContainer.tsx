'use client';
import { useState, useEffect, useRef } from 'react';
import ChatMessage from '@/components/Chat/ChatMessage';
import type { Message } from '@/types';

interface ChatContainerProps {
  messageLogs: Message[];
}

export default function ChatContainer({ messageLogs }: ChatContainerProps) {
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  // useEffect(() => {
  //   if (!conversationId) return;

  //   const fetchMessages = async () => {
  //     setLoading(true);
  //     try {
  //       const conversation = await getConversation(conversationId);
  //       setMessages(conversation.messages || []);
  //     } catch (error) {
  //       console.error('Error fetching messages:', error);
  //     } finally {
  //       setLoading(false);
  //     }
  //   };

  //   fetchMessages();

  //   // Set up polling for new messages
  //   const interval = setInterval(async () => {
  //     try {
  //       const logs = await getChatLogs(conversationId);
  //       // Process logs if needed
  //     } catch (error) {
  //       console.error('Error polling chat logs:', error);
  //     }
  //   }, 3000);

  //   return () => clearInterval(interval);
  // }, [conversationId]);

  // Scroll to bottom when messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messageLogs]);

  if (!messageLogs) {
    return (
      <div className="flex-3 flex items-center justify-center bg-gray-900 text-white">
        Select or create a conversation to start chatting
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex-3 flex items-center justify-center">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="flex-3 overflow-y-auto p-4 bg-gray-900" id="chat-container">
      {messageLogs.length === 0 ? (
        <div className="flex items-center justify-center h-full bg-gray-900 text-gray-500">
          No messages yet. Start by sending a message.
        </div>
      ) : (
        <>
          {messageLogs.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
          <div ref={chatEndRef} />
        </>
      )}
    </div>
  );
}