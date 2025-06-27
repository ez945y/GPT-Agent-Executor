'use client';

interface SidebarHeaderProps {
  onNewChat: () => void;
}

export default function SidebarHeader({ onNewChat }: SidebarHeaderProps) {
  return (
    <div className="bg-gray-700 p-4 bg-opacity-10 bg-black border-b border-white border-opacity-10 flex justify-between items-center">
      <h2 className="text-lg font-medium">Conversations</h2>
      <button 
        onClick={onNewChat}
        className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-white hover:bg-opacity-10 transition-colors"
      >
        <i className="fas fa-plus"></i>
      </button>
    </div>
  );
}