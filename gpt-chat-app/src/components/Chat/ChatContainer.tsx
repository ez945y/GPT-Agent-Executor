'use client';
import { useState, useEffect, useRef } from 'react';
import ChatMessage from '@/components/Chat/ChatMessage';
import type { Message } from '@/types';

interface ChatContainerProps {
  messageLogs: Message[];
}

export default function ChatContainer({ messageLogs }: ChatContainerProps) {
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null)

  // Scroll to bottom when messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messageLogs]);

  if (!messageLogs) {
    return (
      <div className="flex-3 flex items-center justify-center bg-gray-100 text-gray-800">
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
    <div className="flex-3 overflow-y-auto p-4 bg-white" id="chat-container">
      {messageLogs.length === 0 ? (
        <div className="flex items-center justify-center h-full bg-gray-50 text-gray-500">
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