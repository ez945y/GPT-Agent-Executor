'use client';
import { useState, useEffect, useRef } from 'react';
import ThinkItem from '@/components/ThinkLogs/ThinkItem';
import type { LogEntry } from '@/types';

interface ThinkContainerProps {
  conversationLogs: LogEntry[];
  isThinking: boolean;
}

export default function ThinkContainer({ conversationLogs, isThinking }: ThinkContainerProps) {
  // const [ConversationLogs, setConversationLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  
  // Scroll to bottom when new logs are added
  useEffect(() => {
    if (isThinking && containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [conversationLogs, isThinking]);

  if (!conversationLogs) {
    return (
      <div className="flex-2 flex items-center justify-center bg-gray-900 text-white">
        Select or create a conversation to see thinking process
      </div>
    );
  }

  if (loading && conversationLogs.length === 0) {
    return (
      <div className="flex-2 flex items-center justify-center">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div ref={containerRef} className="flex-2 overflow-y-auto p-4 bg-gray-900">
      {conversationLogs.length === 0 ? (
        <div className="flex items-center justify-center h-full text-gray-500">
          No thinking logs available
        </div>
      ) : (
        <>
          {conversationLogs.map((log, index) => (
            <ThinkItem key={index} log={log} />
          ))}
          {/* {isThinking && (
            <div className="flex items-center space-x-2 p-4 text-primary">
              <div className="thinking-indicator inline-flex">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
              <span>Thinking...</span>
            </div>
          )} */}
        </>
      )}
    </div>
  );
}