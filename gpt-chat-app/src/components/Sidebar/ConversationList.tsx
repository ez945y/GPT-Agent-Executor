'use client';
import { format } from 'date-fns';
import type { Conversation } from '@/types';

interface ConversationListProps {
  conversations: Conversation[];
  currentId: string | null;
  onSelect: (id: string) => void;
}

export default function ConversationList({ conversations, currentId, onSelect }: ConversationListProps) {
  if (conversations.length === 0) {
    return (
      <div className="py-4 text-center text-white text-opacity-70">
        No conversations yet
      </div>
    );
  }

  return (
    <ul className="space-y-2">
      {conversations.map((conversation) => {
        const isActive = conversation.id === currentId;
        const formattedDate = format(new Date(conversation.created_at), 'MMM d,део h:mm a');

        return (
          <li 
            key={conversation.id}
            onClick={() => onSelect(conversation.id)}
            className={`
              p-3 rounded-lg cursor-pointer flex items-center
              ${isActive ? 'bg-yellow-500 text-white font-medium' : 'bg-transparent text-white hover:bg-white hover:bg-opacity-10'}
              transition-colors
            `}
          >
            <i className="fas fa-comments mr-3"></i>
            <div className="flex-1 min-w-0">
              <div className="truncate">{conversation.title}</div>
              <div className="text-xs text-opacity-70">{formattedDate}</div>
            </div>
          </li>
        );
      })}
    </ul>
  );
}