import { useState, useEffect, useCallback } from 'react'

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(
    () => !!localStorage.getItem('access_token')
  )

  const login = useCallback((token: string) => {
    localStorage.setItem('access_token', token)
    setIsAuthenticated(true)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('access_token')
    setIsAuthenticated(false)
  }, [])

  useEffect(() => {
    const handleStorage = () => {
      setIsAuthenticated(!!localStorage.getItem('access_token'))
    }
    window.addEventListener('storage', handleStorage)
    return () => window.removeEventListener('storage', handleStorage)
  }, [])

  return { isAuthenticated, login, logout }
}
