import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const sendMessage = async (message, context = []) => {
    try {
        const response = await api.post('/chat', { message, context });
        return response.data;
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
};
