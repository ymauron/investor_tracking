import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Users,
  Building2,
  ArrowRightLeft,
  HandCoins,
  Bookmark,
  Newspaper,
  BellRing,
  LogOut,
} from 'lucide-react'
import { cn } from '@/lib/utils'

const links = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/individuals', icon: Users, label: 'People' },
  { to: '/firms', icon: Building2, label: 'Firms' },
  { to: '/movements', icon: ArrowRightLeft, label: 'Movements' },
  { to: '/deals', icon: HandCoins, label: 'Deals' },
  { to: '/lp-commitments', icon: Bookmark, label: 'LP Commitments' },
  { to: '/transactions', icon: Newspaper, label: 'Transactions' },
  { to: '/alerts', icon: BellRing, label: 'Alerts' },
]

export function Sidebar({ onLogout }: { onLogout: () => void }) {
  return (
    <aside className="w-56 h-screen bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col">
      <div className="p-4 border-b border-gray-200 dark:border-gray-800">
        <h1 className="text-lg font-bold tracking-tight">Investor Tracker</h1>
        <p className="text-xs text-gray-500">Healthcare LP/GP</p>
      </div>

      <nav className="flex-1 p-3 space-y-1">
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-brand-50 dark:bg-brand-900/20 text-brand-700 dark:text-brand-300'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              )
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="p-3 border-t border-gray-200 dark:border-gray-800">
        <button
          onClick={onLogout}
          className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 w-full transition-colors"
        >
          <LogOut size={16} />
          Logout
        </button>
      </div>
    </aside>
  )
}
