import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search } from 'lucide-react'
import { useDebounce } from '@/hooks/useDebounce'
import { listFirms } from '@/api/firms'
import { FIRM_TYPES } from '@/lib/constants'
import type { ManagementCompany } from '@/types'

export function FirmsListPage() {
  const [firms, setFirms] = useState<ManagementCompany[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [typeFilter, setTypeFilter] = useState('')
  const debouncedSearch = useDebounce(searchQuery, 300)
  const navigate = useNavigate()

  useEffect(() => {
    setLoading(true)
    listFirms({
      search: debouncedSearch || undefined,
      firm_type: typeFilter || undefined,
    })
      .then(setFirms)
      .finally(() => setLoading(false))
  }, [debouncedSearch, typeFilter])

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Firms</h2>
        <div className="flex items-center gap-3">
          <div className="relative">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Filter by name..."
              className="pl-8 pr-3 py-1.5 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>
          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="px-3 py-1.5 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-brand-500"
          >
            <option value="">All Types</option>
            {FIRM_TYPES.map((t) => (
              <option key={t.value} value={t.value}>{t.label}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>
        ) : firms.length === 0 ? (
          <div className="flex items-center justify-center h-64 text-gray-400">No firms found</div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-800">
                <th className="text-left py-3 px-4 font-medium text-gray-500">Name</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Type</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Location</th>
              </tr>
            </thead>
            <tbody>
              {firms.map((firm) => (
                <tr
                  key={firm.id}
                  onClick={() => navigate(`/firms/${firm.id}`)}
                  className="border-b border-gray-100 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-900 cursor-pointer transition-colors"
                >
                  <td className="py-3 px-4 font-medium">{firm.name}</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 rounded-full text-xs bg-brand-50 dark:bg-brand-900/20 text-brand-700 dark:text-brand-300">
                      {firm.firm_type.replace(/_/g, ' ').toUpperCase()}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-gray-500">
                    {firm.hq_city && firm.hq_state ? `${firm.hq_city}, ${firm.hq_state}` : '—'}
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
