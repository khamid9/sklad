import api from './client'
export const getUsers = (params) => api.get('/admin/users', { params })
export const getAdminProducts = (params) => api.get('/admin/products', { params })
export const getAdminStatistics = () => api.get('/admin/statistics')
export const approveUser = id => api.patch(`/admin/users/${id}/approve`)
export const deleteUser = id => api.delete(`/admin/users/${id}`)
