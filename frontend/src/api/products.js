import api from './client'
const toApi = ({ sku, price, ...product }) => ({ ...product, article_number: product.article_number || sku || null, barcode: product.barcode || null, category_id: product.category_id ? Number(product.category_id) : null, purchase_price: Number(product.purchase_price || 0), sale_price: Number(product.sale_price ?? price ?? 0), quantity: Number(product.quantity || 0), min_quantity: Number(product.min_quantity || 0) })
const fromApi = ({ article_number, sale_price, ...product }) => ({ ...product, sku: article_number, price: sale_price, article_number, sale_price })
export const getProducts = async (params) => { const response = await api.get('/products', { params }); return { ...response, data: Array.isArray(response.data) ? response.data.map(fromApi) : response.data } }
export const getProduct = async id => { const response = await api.get(`/products/${id}`); return { ...response, data: fromApi(response.data) } }
export const getCategories = () => api.get('/categories')
export const createProduct = (payload) => api.post('/products', toApi(payload))
export const updateProduct = (id, payload) => api.put(`/products/${id}`, toApi(payload))
export const deleteProduct = (id) => api.delete(`/products/${id}`)
export const getByBarcode = (barcode) => api.get(`/products/barcode/${barcode}`)
