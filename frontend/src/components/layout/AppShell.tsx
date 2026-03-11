import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'
import { SearchBar } from './SearchBar'
import { ThemeToggle } from './ThemeToggle'
import { NotificationBell } from '../NotificationBell'

export function AppShell({ onLogout }: { onLogout: () => void }) {
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar onLogout={onLogout} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-14 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between px-6 bg-white dark:bg-gray-950">
          <SearchBar />
          <div className="flex items-center gap-2">
            <NotificationBell />
            <ThemeToggle />
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
