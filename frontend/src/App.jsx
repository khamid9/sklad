import { Navigate, Route, Routes } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import AppLayout from './layouts/AppLayout'
import AuthPage from './pages/AuthPage'
import DashboardPage from './pages/DashboardPage'
import ProductsPage from './pages/ProductsPage'
import ProductFormPage from './pages/ProductFormPage'
import OperationsPage from './pages/OperationsPage'
import HistoryPage from './pages/HistoryPage'
import StatisticsPage from './pages/StatisticsPage'
import AdminPage from './pages/AdminPage'
import ProfilePage from './pages/ProfilePage'
import SimplePage from './pages/SimplePage'

function Protected({ children, admin = false }) {
  const { isAuthenticated, user } = useAuth()
  if (!isAuthenticated) return <Navigate to="/login" replace />
  return admin && user?.role !== 'admin' ? <Navigate to="/dashboard" replace /> : children
}

export default function App() {
  return <Routes><Route path="/login" element={<AuthPage mode="login" />} /><Route path="/register" element={<AuthPage mode="register" />} /><Route element={<Protected><AppLayout /></Protected>}><Route path="/dashboard" element={<DashboardPage />} /><Route path="/products" element={<ProductsPage />} /><Route path="/products/create" element={<ProductFormPage />} /><Route path="/products/edit/:id" element={<ProductFormPage />} /><Route path="/products/:id" element={<SimplePage title="Карточка товара" description="Партии, продажи и история выбранного товара." />} /><Route path="/batches" element={<OperationsPage type="batches" />} /><Route path="/sales" element={<OperationsPage type="sales" />} /><Route path="/history" element={<HistoryPage />} /><Route path="/statistics" element={<StatisticsPage />} /><Route path="/profile" element={<ProfilePage />} /><Route path="/admin" element={<Protected admin><AdminPage /></Protected>} /><Route path="/admin/requests" element={<Protected admin><AdminPage requestsOnly /></Protected>} /></Route><Route path="*" element={<Navigate to="/dashboard" replace />} /></Routes>
}
