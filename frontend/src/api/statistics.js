import api from './client'
export const getDayStatistics = () => api.get('/statistics/day')
export const getWeekStatistics = () => api.get('/statistics/week')
export const getMonthStatistics = () => api.get('/statistics/month')
export const getTopProducts = () => api.get('/statistics/top-products')
