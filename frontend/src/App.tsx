import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { LoginPage } from '@/pages/LoginPage'
import { DashboardPage } from '@/pages/DashboardPage'
import { DirectoryPage } from '@/pages/DirectoryPage'
import { IndividualPage } from '@/pages/IndividualPage'
import { FirmsListPage } from '@/pages/FirmsListPage'
import { FirmPage } from '@/pages/FirmPage'
import { MovementsPage } from '@/pages/MovementsPage'
import { DealsPage } from '@/pages/DealsPage'
import { LPCommitmentsPage } from '@/pages/LPCommitmentsPage'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 1,
    },
  },
})

export default function App() {
  const { isAuthenticated, login, logout } = useAuth()

  if (!isAuthenticated) {
    return <LoginPage onLogin={login} />
  }

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<AppShell onLogout={logout} />}>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/individuals" element={<DirectoryPage />} />
            <Route path="/individuals/:id" element={<IndividualPage />} />
            <Route path="/firms" element={<FirmsListPage />} />
            <Route path="/firms/:id" element={<FirmPage />} />
            <Route path="/movements" element={<MovementsPage />} />
            <Route path="/deals" element={<DealsPage />} />
            <Route path="/lp-commitments" element={<LPCommitmentsPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
