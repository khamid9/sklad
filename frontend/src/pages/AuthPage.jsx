import { Box, Eye, EyeOff, LockKeyhole, Mail, UserRound } from 'lucide-react'
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register } from '../api/auth'
import { getErrorMessage } from '../api/client'
import { useAuth } from '../context/AuthContext'

export default function AuthPage({ mode }) {
  const isLogin = mode === 'login'
  const navigate = useNavigate()
  const { login } = useAuth()
  const [form, setForm] = useState({ name: '', email: '', password: '', password_confirmation: '' })
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const change = event => setForm({ ...form, [event.target.name]: event.target.value })
  const submit = async event => {
    event.preventDefault(); setError('')
    if (!isLogin && form.password !== form.password_confirmation) return setError('Пароли не совпадают.')
    setLoading(true)
    try { if (isLogin) { await login({ email: form.email, password: form.password }); navigate('/dashboard') } else { await register({ name: form.name, email: form.email, password: form.password }); navigate('/login') }
    } catch (err) { setError(getErrorMessage(err)) } finally { setLoading(false) }
  }
  const passwordField = (name, label, placeholder) => <label>{label}<div className="input"><LockKeyhole size={18}/><input type={showPassword ? 'text' : 'password'} name={name} required minLength="6" value={form[name]} onChange={change} placeholder={placeholder}/><button type="button" className="password-toggle" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? 'Скрыть пароль' : 'Показать пароль'}>{showPassword ? <EyeOff size={18}/> : <Eye size={18}/>}</button></div></label>
  return <div className="auth-page"><section className="auth-promo"><div className="promo-brand"><Box/> Мой Склад</div><div><span className="eyebrow">УПРАВЛЯЙТЕ ЛЕГКО</span><h1>Ваш склад.<br/><em>Всё под контролем.</em></h1><p>Товары, поставки и продажи — в одном понятном сервисе.</p></div></section><main className="auth-form-wrap"><form className="auth-form" onSubmit={submit}><div className="mobile-brand"><Box/> Мой Склад</div><span className="eyebrow">{isLogin ? 'С ВОЗВРАЩЕНИЕМ' : 'НОВЫЙ АККАУНТ'}</span><h2>{isLogin ? 'Войдите в аккаунт' : 'Создайте аккаунт'}</h2><p>{isLogin ? 'Введите данные, чтобы продолжить работу.' : 'Начните управлять складом за пару минут.'}</p>{error && <div className="form-error">{error}</div>}{!isLogin && <label>Имя<div className="input"><UserRound size={18}/><input name="name" required value={form.name} onChange={change} placeholder="Ваше имя"/></div></label>}<label>Email<div className="input"><Mail size={18}/><input type="email" name="email" required value={form.email} onChange={change} placeholder="name@example.com"/></div></label>{passwordField('password', 'Пароль', 'Минимум 6 символов')}{!isLogin && passwordField('password_confirmation', 'Подтвердите пароль', 'Повторите пароль')}<button className="primary full" disabled={loading}>{loading ? 'Подождите...' : isLogin ? 'Войти' : 'Зарегистрироваться'}</button><p className="auth-switch">{isLogin ? 'Нет аккаунта?' : 'Уже есть аккаунт?'} <Link to={isLogin ? '/register' : '/login'}>{isLogin ? 'Зарегистрироваться' : 'Войти'}</Link></p></form></main></div>
}
