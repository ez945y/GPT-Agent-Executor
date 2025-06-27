import axios from 'axios';
import type { Conversation } from '@/types';

const API_URL = 'http://127.0.0.1:8000/api';

export const getConversations = async (): Promise<Conversation[]> => {
  const response = await axios.get(`${API_URL}/conversations`);
  console.log(response.data);
  return response.data;
};

export const getConversation = async (id: string): Promise<Conversation> => {
  const response = await axios.get(`${API_URL}/conversations/${id}`);
  return response.data;
};

export const createConversation = async (): Promise<{ conversation_id: string }> => {
  const response = await axios.post(`${API_URL}/conversations`);
  return response.data;
};

export const updateConversationTitle = async (id: string, title: string): Promise<void> => {
  await axios.put(`${API_URL}/conversations/${id}/title`, { title });
};

export const deleteConversation = async (id: string): Promise<void> => {
  await axios.delete(`${API_URL}/conversations/${id}`);
};

export const exportConversation = async (id: string, format: 'json' | 'text' = 'json') => {
  const response = await axios.get(`${API_URL}/export/${id}?format=${format}`);
  return response.data;
};