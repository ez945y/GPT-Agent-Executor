export interface Message {
    role: 'user' | 'assistant';
    message: string;
    timestamp: string;
    sequence: string;
  }
  
  export interface LogEntry {
    timestamp: string;
    sequence: string;
    message: string;
  }
  
  export interface Conversation {
    id: string;
    title: string;
    messages: Message[];
    think_logs?: LogEntry[];
    chat_logs?: LogEntry[];
    created_at: string;
  }
  
  export interface Settings {
    theme: 'light' | 'dark';
    notification_sound: boolean;
    max_history: number;
  }