import { BarChart3, TrendingUp } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getMonthStatistics, getTopProducts } from '../api/statistics'
import { getErrorMessage } from '../api/client'

const money = value => `${new Intl.NumberFormat('ru-RU').format(value || 0)} сом`
export default function StatisticsPage() {
  const [stats, setStats] = useState(null)
  const [top, setTop] = useState([])
  const [error, setError] = useState('')
  useEffect(() => { Promise.all([getMonthStatistics(), getTopProducts()]).then(([statsResponse, topResponse]) => { setStats(statsResponse.data); setTop(topResponse.data) }).catch(err => setError(getErrorMessage(err))) }, [])
  return <><header className="page-head"><div><span className="eyebrow">АНАЛИТИКА</span><h1>Статистика</h1><p>Продажи и выручка за последние 30 дней.</p></div></header>{error && <div className="form-error">{error}</div>}<section className="stats-grid"><article className="stat-card"><div><p>Продаж</p><h2>{stats?.sales_count || 0}</h2><small>за месяц</small></div><div className="stat-icon"><BarChart3 size={19}/></div></article><article className="stat-card green"><div><p>Выручка</p><h2>{money(stats?.revenue)}</h2><small>за месяц</small></div><div className="stat-icon"><TrendingUp size={19}/></div></article><article className="stat-card violet"><div><p>Продано единиц</p><h2>{stats?.sold_quantity || 0}</h2><small>товаров</small></div><div className="stat-icon">#</div></article><article className="stat-card orange"><div><p>Прибыль</p><h2>{money(stats?.profit)}</h2><small>за месяц</small></div><div className="stat-icon">↗</div></article></section><section className="panel statistics-panel"><div className="panel-title"><div><h3>Самые продаваемые товары</h3><p>Рейтинг за текущий месяц</p></div></div>{top.length ? <ol className="top-list">{top.map((item, index) => <li key={item.name}><span className={`place p${index + 1}`}>{index + 1}</span><b>{item.name}</b><small>{item.quantity} шт.</small></li>)}</ol> : <div className="empty-state"><div>○</div><h3>Данных пока нет</h3><p>Продажи появятся в аналитике после оформления.</p></div>}</section></>
}
