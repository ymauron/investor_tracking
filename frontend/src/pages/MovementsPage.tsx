import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { formatDate } from '@/lib/utils'
import api from '@/api/client'
import type { MovementEvent } from '@/types'

export function MovementsPage() {
  const [movements, setMovements] = useState<MovementEvent[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    api.get('/movements', { params: { per_page: 100 } })
      .then(({ data }) => setMovements(data))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <h2 className="text-lg font-semibold mb-6">Movement Events</h2>
      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>
        ) : movements.length === 0 ? (
          <div className="flex items-center justify-center h-64 text-gray-400">No movements found</div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-800">
                <th className="text-left py-3 px-4 font-medium text-gray-500">Type</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Date</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Confidence</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Tags</th>
              </tr>
            </thead>
            <tbody>
              {movements.map((m) => (
                <tr
                  key={m.id}
                  onClick={() => navigate(`/individuals/${m.individual_id}`)}
                  className="border-b border-gray-100 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-900 cursor-pointer transition-colors"
                >
                  <td className="py-3 px-4">
                    <span className="font-medium">{m.move_type}</span>
                    {m.is_spinout && (
                      <span className="ml-2 px-1.5 py-0.5 rounded text-xs bg-purple-100 dark:bg-purple-900/20 text-purple-700">Spinout</span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-gray-500">
                    {m.joining_date ? formatDate(m.joining_date) : m.departure_date ? formatDate(m.departure_date) : '—'}
                  </td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 rounded-full text-xs bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400">
                      {m.confidence}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex gap-1">
                      {m.tags.map((t) => (
                        <span key={t} className="px-1.5 py-0.5 rounded text-xs bg-amber-100 dark:bg-amber-900/20 text-amber-700">
                          {t}
                        </span>
                      ))}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
