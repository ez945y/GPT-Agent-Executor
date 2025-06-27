'use client';
import { format } from 'date-fns';
import type { Message } from '@/types';

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  const formattedTime = message.timestamp ? format(new Date(message.timestamp), 'HH:mm') : '';
  
  return (
    <div className={`chat-message flex ${isUser ? 'flex-row-reverse' : 'flex-row'} mb-4`}>
      <div className={`avatar flex-shrink-0 ${isUser ? 'ml-3' : 'mr-3'} w-10 h-10 rounded-full flex items-center justify-center bg-gray-300 text-gray-700`}>
        {isUser ? 'U' : 'A'}
      </div>
      <div className={`message max-w-[80%] p-3 rounded-lg shadow-sm ${isUser ? 'bg-gray-200 text-gray-800' : 'bg-gray-200 text-gray-800'}`}>
        <div className="whitespace-pre-wrap">{message.message || message.content}</div>
        {formattedTime && <div className="timestamp text-xs mt-1 text-gray-500">{formattedTime}</div>}
      </div>
    </div>
  );
}