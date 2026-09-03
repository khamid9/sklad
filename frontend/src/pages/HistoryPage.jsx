import { ClipboardList } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getHistory } from '../api/history'
import { getErrorMessage } from '../api/client'

export default function HistoryPage() {
  const [items, setItems] = useState([])
  const [error, setError] = useState('')
  useEffect(() => { getHistory().then(response => setItems(response.data)).catch(err => setError(getErrorMessage(err))) }, [])
  return <><header className="page-head"><div><span className="eyebrow">КОНТРОЛЬ</span><h1>История операций</h1><p>Все приходы, продажи и изменения остатков в одном журнале.</p></div></header>{error && <div className="form-error">{error}</div>}<section className="panel"><div className="panel-title"><div><h3>Журнал склада</h3><p>{items.length ? `${items.length} операций` : 'Операции появятся после первой поставки или продажи'}</p></div><ClipboardList size={21}/></div>{items.length ? <div className="table-wrap"><table><thead><tr><th>Дата</th><th>Операция</th><th>Описание</th><th>Количество</th></tr></thead><tbody>{items.map(item => <tr key={item.id}><td>{new Date(item.created_at).toLocaleString('ru-RU')}</td><td><span className="tag">{item.operation_type}</span></td><td>{item.description}</td><td>{item.quantity ? `${item.quantity} шт.` : '-'}</td></tr>)}</tbody></table></div> : <div className="empty-state"><div>○</div><h3>История пока пуста</h3><p>После первой операции записи появятся здесь.</p></div>}</section></>
}
