import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

export const getSettings = async () => {
  const response = await axios.get(`${API_URL}/settings`);
  return response.data;
};

export const updateSettings = async (settings: any) => {
  const response = await axios.put(`${API_URL}/settings`, settings);
  return response.data;
};