import { ChevronLeft, ChevronRight, Edit3, Eye, Plus, Search, Trash2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { deleteProduct, getProducts } from '../api/products'

const pageSize = 50
export default function ProductsPage() {
  const [products, setProducts] = useState([])
  const [query, setQuery] = useState('')
  const [page, setPage] = useState(0)
  const [total, setTotal] = useState(0)
  const [notice, setNotice] = useState('')
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    const timer = setTimeout(() => getProducts({ search: query || undefined, limit: pageSize, offset: page * pageSize }).then(response => { setProducts(response.data.items || response.data); setTotal(response.data.total ?? response.data.length) }).catch(() => setNotice('Не удалось загрузить каталог. Проверьте подключение к API.')).finally(() => setLoading(false)), 250)
    return () => clearTimeout(timer)
  }, [query, page])
  const remove = async id => { if (!window.confirm('Удалить товар? Это действие нельзя отменить.')) return; try { await deleteProduct(id); setProducts(products.filter(product => product.id !== id)); setTotal(total - 1); setNotice('Товар удалён.') } catch (error) { setNotice(error.response?.data?.detail || 'Не удалось удалить товар.') } }
  const pageCount = Math.max(1, Math.ceil(total / pageSize))
  return <><header className="page-head"><div><span className="eyebrow">КАТАЛОГ</span><h1>Товары</h1><p>Управляйте остатками и данными товаров.</p></div><Link className="primary" to="/products/create"><Plus size={18}/> Добавить товар</Link></header>{notice && <div className="demo-note">{notice}</div>}<section className="panel"><div className="table-tools"><div className="search"><Search size={18}/><input value={query} onChange={event => { setQuery(event.target.value); setPage(0) }} placeholder="Найти товар, артикул или штрих-код"/></div><span className="muted">Всего: {total}</span></div><div className="table-wrap"><table><thead><tr><th>Товар</th><th>Артикул</th><th>Штрих-код</th><th>Категория</th><th>Цена</th><th>Остаток</th><th /></tr></thead><tbody>{loading ? <tr><td colSpan="7">Загрузка каталога...</td></tr> : products.map(product => <tr key={product.id}><td><div className="product-cell"><span className="product-dot">{product.name[0]}</span><b>{product.name}</b></div></td><td>{product.article_number || '-'}</td><td>{product.barcode || '-'}</td><td><span className="tag">{product.category?.name || 'Без категории'}</span></td><td>{product.sale_price} сом</td><td><b className={product.quantity <= product.min_quantity ? 'danger' : ''}>{product.quantity} шт.</b></td><td><div className="row-actions"><Link to={`/products/${product.id}`} title="Открыть"><Eye size={17}/></Link><Link to={`/products/edit/${product.id}`} title="Изменить"><Edit3 size={17}/></Link><button onClick={() => remove(product.id)} title="Удалить"><Trash2 size={17}/></button></div></td></tr>)}{!loading && !products.length && <tr><td colSpan="7">Товары не найдены.</td></tr>}</tbody></table></div><div className="pagination"><span>Страница {page + 1} из {pageCount}</span><div><button className="secondary" disabled={page === 0} onClick={() => setPage(page - 1)}><ChevronLeft size={17}/></button><button className="secondary" disabled={page + 1 >= pageCount} onClick={() => setPage(page + 1)}><ChevronRight size={17}/></button></div></div></section></>
}
