import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

export const sendMessage = async (message: string, conversationId: string) => {
  const response = await axios.post(`${API_URL}/send_message`, { message }, {
    params: { conversation_id: conversationId }
  });
  return response.data;
};

export const searchMessages = async (query: string) => {
  const response = await axios.get(`${API_URL}/search`, {
    params: { query }
  });
  return response.data;
};