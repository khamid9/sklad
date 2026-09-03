import { ArrowLeft, Save } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { createProduct, getCategories, getProduct, updateProduct } from '../api/products'
import { getErrorMessage } from '../api/client'

const initial = { name: '', article_number: '', barcode: '', category_id: '', purchase_price: '', sale_price: '', quantity: 0, min_quantity: 10, description: '' }

export default function ProductFormPage() {
  const { id } = useParams()
  const edit = Boolean(id)
  const [form, setForm] = useState(initial)
  const [categories, setCategories] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(edit)
  const navigate = useNavigate()

  useEffect(() => {
    Promise.all([getCategories(), edit ? getProduct(id) : Promise.resolve(null)])
      .then(([categoryResponse, productResponse]) => {
        setCategories(categoryResponse.data)
        if (productResponse) setForm({ ...initial, ...productResponse.data, category_id: productResponse.data.category_id || '' })
      })
      .catch(err => setError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [edit, id])

  const change = event => setForm({ ...form, [event.target.name]: event.target.value })
  const submit = async event => {
    event.preventDefault(); setLoading(true); setError('')
    try { if (edit) await updateProduct(id, form); else await createProduct(form); navigate('/products') }
    catch (err) { setError(getErrorMessage(err)); setLoading(false) }
  }

  return <><header className="page-head"><div><Link className="back" to="/products"><ArrowLeft size={17}/> К товарам</Link><h1>{edit ? 'Редактировать товар' : 'Новый товар'}</h1><p>Заполните данные, чтобы товар находился по сканеру и артикулу.</p></div></header><form className="panel form-card" onSubmit={submit}>{error && <div className="form-error">{error}</div>}<div className="form-grid"><label>Название товара<input required name="name" value={form.name} onChange={change} placeholder="Например, Coca-Cola 1L"/></label><label>Артикул<input name="article_number" value={form.article_number || ''} onChange={change} placeholder="COC001"/></label><label>Штрих-код<input name="barcode" value={form.barcode || ''} onChange={change} placeholder="4870001234567"/></label><label>Категория<select name="category_id" value={form.category_id} onChange={change}><option value="">Без категории</option>{categories.map(category => <option key={category.id} value={category.id}>{category.name}</option>)}</select></label><label>Цена закупки, сом<input type="number" min="0" step="0.01" name="purchase_price" value={form.purchase_price} onChange={change}/></label><label>Цена продажи, сом<input required type="number" min="0" step="0.01" name="sale_price" value={form.sale_price} onChange={change}/></label>{!edit && <label>Начальный остаток, шт.<input type="number" min="0" name="quantity" value={form.quantity} onChange={change}/></label>}<label>Минимальный остаток, шт.<input type="number" min="0" name="min_quantity" value={form.min_quantity} onChange={change}/></label><label className="wide">Описание<textarea name="description" value={form.description || ''} onChange={change} placeholder="Необязательно" rows="4"/></label></div><div className="form-actions"><Link className="secondary" to="/products">Отмена</Link><button type="submit" className="primary" disabled={loading}><Save size={17}/>{loading ? 'Сохраняем...' : edit ? 'Сохранить изменения' : 'Добавить товар'}</button></div></form></>
}
