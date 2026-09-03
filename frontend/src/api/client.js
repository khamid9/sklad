import axios from 'axios'
const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000' })
api.interceptors.request.use((config) => { const token = localStorage.getItem('sklad_token'); if (token) config.headers.Authorization = `Bearer ${token}`; return config })
export const getErrorMessage = (error) => error.response?.data?.detail || 'Не удалось выполнить запрос. Попробуйте ещё раз.'
export default api
