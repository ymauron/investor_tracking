import { useState, useEffect } from 'react'
import { formatDate, formatArea } from '@/lib/utils'
import api from '@/api/client'
import type { Deal } from '@/types'

export function DealsPage() {
  const [deals, setDeals] = useState<Deal[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/deals', { params: { per_page: 100 } })
      .then(({ data }) => setDeals(data))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <h2 className="text-lg font-semibold mb-6">Deals</h2>
      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>
        ) : deals.length === 0 ? (
          <div className="flex items-center justify-center h-64 text-gray-400">No deals found</div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-800">
                <th className="text-left py-3 px-4 font-medium text-gray-500">Name</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Type</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Area</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Size ($M)</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Date</th>
              </tr>
            </thead>
            <tbody>
              {deals.map((d) => (
                <tr key={d.id} className="border-b border-gray-100 dark:border-gray-800/50">
                  <td className="py-3 px-4 font-medium">{d.name}</td>
                  <td className="py-3 px-4">
                    {d.deal_type && (
                      <span className="px-2 py-0.5 rounded-full text-xs bg-gray-100 dark:bg-gray-800 text-gray-600">
                        {d.deal_type.replace(/_/g, ' ')}
                      </span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-gray-500">{formatArea(d.therapeutic_area)}</td>
                  <td className="py-3 px-4 text-gray-500">{d.deal_size_mm ? `$${d.deal_size_mm}` : '—'}</td>
                  <td className="py-3 px-4 text-gray-500 text-xs">{d.deal_date ? formatDate(d.deal_date) : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
