'use client';
import { format } from 'date-fns';
import type { Message } from '@/types';

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  const formattedTime = format(new Date(message.timestamp), 'HH:mm');
  console.log(message);
  return (
   
    <div className={`chat-message flex ${isUser ? 'flex-row-reverse' : 'flex-row'} mb-4`}>
      <div className={`avatar flex-shrink-0 ${isUser ? 'ml-3' : 'mr-3'} w-10 h-10 rounded-full flex items-center justify-center bg-gray-700 text-white`}>
        {isUser ? 'U' : 'A'}
      </div>
      <div className={`message max-w-[80%] p-3 rounded-lg ${isUser ? 'bg-primary text-white' : 'bg-light-bg'}`}>
        <div>{message.message}</div>
        <div className="timestamp text-xs mt-1 opacity-70">{formattedTime}</div>
      </div>
    </div>
  );
}