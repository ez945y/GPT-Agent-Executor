import axios from 'axios';
import type { LogEntry } from '@/types';

const API_URL = 'http://127.0.0.1:8000/api';

export const getThinkLogs = async (conversationId?: string): Promise<LogEntry[]> => {
  const params = conversationId ? { conversation_id: conversationId } : {};
  const response = await axios.get(`${API_URL}/think_logs`, { params });
  return response.data;
};

export const getToolLogs = async (conversationId?: string): Promise<LogEntry[]> => {
  const params = conversationId ? { conversation_id: conversationId } : {};
  const response = await axios.get(`${API_URL}/tool_logs`, { params });
  return response.data;
};

export const getChatLogs = async (conversationId?: string): Promise<LogEntry[]> => {
  const params = conversationId ? { conversation_id: conversationId } : {};
  const response = await axios.get(`${API_URL}/chat_logs`, { params });
  return response.data;
};