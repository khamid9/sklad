import { LogOut, UserRound } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function ProfilePage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const exit = () => { logout(); navigate('/login') }
  return <><header className="page-head"><div><span className="eyebrow">АККАУНТ</span><h1>Профиль</h1><p>Данные пользователя и доступ к складу.</p></div></header><section className="panel profile-card"><div className="profile-avatar"><UserRound size={30}/></div><div><h3>{user?.name || 'Пользователь'}</h3><p>{user?.email || 'Email не указан'}</p><span className="tag">{user?.role === 'admin' ? 'Администратор' : 'Владелец склада'}</span></div></section><button className="secondary profile-logout" onClick={exit}><LogOut size={17}/> Выйти из аккаунта</button></>
}
