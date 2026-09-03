import { Barcode, Calculator, PackagePlus, ShoppingCart } from 'lucide-react'
import { useRef, useState } from 'react'
import { addBatch, createSale, findProducts } from '../api/operations'
import { getErrorMessage } from '../api/client'

export default function OperationsPage({ type }) {
  const batch = type === 'batches'
  const inputRef = useRef(null)
  const [form, setForm] = useState({ product: '', product_id: '', batch_number: '', boxes: '', items_per_box: '', quantity: '' })
  const [product, setProduct] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [searching, setSearching] = useState(false)

  const change = event => setForm({ ...form, [event.target.name]: event.target.value })
  const total = Number(form.boxes || 0) * Number(form.items_per_box || 0)

  const lookup = async () => {
    if (!form.product.trim()) return false
    setSearching(true)
    setError('')
    try {
      const response = await findProducts(form.product.trim())
      const results = Array.isArray(response.data) ? response.data : response.data.items || []
      if (results.length !== 1) throw new Error(results.length ? 'Найдено несколько товаров. Уточните запрос.' : 'Товар не найден.')
      const found = results[0]
      setProduct(found)
      setForm(current => ({ ...current, product_id: found.id }))
      return true
    } catch (err) {
      setProduct(null)
      setError(err.response ? getErrorMessage(err) : err.message)
      return false
    } finally { setSearching(false) }
  }

  const submit = async event => {
    event.preventDefault()
    setError('')
    setMessage('')
    try {
      if (!form.product_id && !(await lookup())) return
      if (batch) {
        await addBatch(form.product_id, { batch_number: form.batch_number || null, boxes: Number(form.boxes), items_per_box: Number(form.items_per_box) })
        setMessage(`Партия добавлена: ${total} шт.`)
      } else {
        await createSale({ product_id: Number(form.product_id), quantity: Number(form.quantity) })
        setMessage(`Продажа оформлена. Остаток уменьшен на ${form.quantity} шт.`)
      }
      setForm({ product: '', product_id: '', batch_number: '', boxes: '', items_per_box: '', quantity: '' })
      setProduct(null)
      inputRef.current?.focus()
    } catch (err) { setError(getErrorMessage(err)) }
  }

  return <>
    <header className="page-head"><div><span className="eyebrow">ОПЕРАЦИИ</span><h1>{batch ? 'Приём партии' : 'Оформление продажи'}</h1><p>{batch ? 'Отсканируйте товар или найдите его вручную.' : 'Продажа автоматически уменьшит остаток на складе.'}</p></div></header>
    <form className="panel operation-form" onSubmit={submit}>
      {error && <div className="form-error">{error}</div>}
      {message && <div className="success-note">✓ {message}</div>}
      <label>Штрих-код, артикул или ID товара<div className="lookup-row"><input ref={inputRef} name="product" required value={form.product} onChange={change} onBlur={lookup} onKeyDown={event => event.key === 'Enter' && (event.preventDefault(), lookup())} placeholder="Сканируйте или введите номер"/><button type="button" className="barcode-button icon-action" onClick={() => inputRef.current?.focus()} title="Фокус на поле сканирования"><Barcode size={19}/></button></div></label>
      {product && <div className="selected-product"><div className="product-dot">{product.name[0]}</div><div><b>{product.name}</b><small>Остаток: {product.quantity} шт. | Артикул: {product.article_number || 'не указан'}</small></div></div>}
      {batch ? <><div className="form-grid"><label>Номер партии<input name="batch_number" value={form.batch_number} onChange={change} placeholder="Необязательно"/></label><label>Количество коробок<input required min="1" type="number" name="boxes" value={form.boxes} onChange={change} placeholder="5"/></label><label>Товаров в коробке<input required min="1" type="number" name="items_per_box" value={form.items_per_box} onChange={change} placeholder="24"/></label></div><div className="calculation"><Calculator size={20}/><span>{form.boxes || 0} коробок × {form.items_per_box || 0} шт. = <b>{total} шт.</b></span></div><button className="primary" disabled={searching}><PackagePlus size={18}/>{searching ? 'Ищем товар...' : 'Добавить партию'}</button></> : <><label>Количество, шт.<input required min="1" type="number" name="quantity" value={form.quantity} onChange={change} placeholder="1"/></label><button className="primary" disabled={searching}><ShoppingCart size={18}/>{searching ? 'Ищем товар...' : 'Оформить продажу'}</button></>}
    </form>
  </>
}
