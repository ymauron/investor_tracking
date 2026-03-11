import { useState, useEffect, useRef } from 'react'
import { Bell } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { getUnreadCount, listNotifications, markAsRead, markAllAsRead } from '@/api/alerts'
import { formatDate } from '@/lib/utils'
import type { AlertNotification } from '@/types'

export function NotificationBell() {
  const [count, setCount] = useState(0)
  const [open, setOpen] = useState(false)
  const [notifications, setNotifications] = useState<AlertNotification[]>([])
  const navigate = useNavigate()
  const ref = useRef<HTMLDivElement>(null)

  const loadCount = () => {
    getUnreadCount().then(setCount).catch(() => {})
  }

  useEffect(() => {
    loadCount()
    const interval = setInterval(loadCount, 60_000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleOpen = () => {
    if (!open) {
      listNotifications({ unread_only: true, per_page: 10 }).then(setNotifications)
    }
    setOpen(!open)
  }

  const handleClick = async (notif: AlertNotification) => {
    if (!notif.is_read) {
      await markAsRead(notif.id)
      loadCount()
    }
    setOpen(false)
    navigate(`/transactions/${notif.transaction_id}`)
  }

  const handleMarkAllRead = async () => {
    await markAllAsRead()
    setCount(0)
    setNotifications(n => n.map(x => ({ ...x, is_read: true })))
  }

  return (
    <div ref={ref} className="relative">
      <button
        onClick={handleOpen}
        className="relative p-2 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
      >
        <Bell size={18} />
        {count > 0 && (
          <span className="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] flex items-center justify-center rounded-full bg-red-500 text-white text-[10px] font-bold px-1">
            {count > 99 ? '99+' : count}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-1 w-80 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50">
          <div className="flex items-center justify-between px-3 py-2 border-b border-gray-200 dark:border-gray-800">
            <span className="text-xs font-semibold text-gray-500 uppercase">Notifications</span>
            {count > 0 && (
              <button
                onClick={handleMarkAllRead}
                className="text-xs text-brand-600 hover:underline"
              >
                Mark all read
              </button>
            )}
          </div>
          <div className="max-h-80 overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="px-3 py-6 text-center text-sm text-gray-400">No unread notifications</div>
            ) : (
              notifications.map((n) => (
                <button
                  key={n.id}
                  onClick={() => handleClick(n)}
                  className="w-full px-3 py-2.5 text-left hover:bg-gray-50 dark:hover:bg-gray-800 border-b border-gray-100 dark:border-gray-800/50 last:border-0"
                >
                  <div className="text-sm font-medium truncate">{n.transaction.title}</div>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-xs text-brand-600">{n.alert_rule_name}</span>
                    <span className="text-xs text-gray-400">{formatDate(n.created_at)}</span>
                  </div>
                </button>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}
