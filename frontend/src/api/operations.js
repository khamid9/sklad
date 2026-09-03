import api from './client'
export const addBatch = (productId, payload) => api.post(`/products/${productId}/batches`, payload)
export const createSale = (payload) => api.post('/sales', payload)
export const findProducts = (search) => api.get('/products', { params: { search } })
export const getDashboard = () => api.get('/dashboard')
