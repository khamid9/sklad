import api from './client'
export const getHistory = (params) => api.get('/history', { params })
