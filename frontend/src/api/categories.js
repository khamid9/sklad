import api from './client'
export const getCategories = () => api.get('/categories')
export const createCategory = (payload) => api.post('/categories', payload)
