import { useState, useEffect } from 'react'
import { formatDate } from '@/lib/utils'
import api from '@/api/client'
import type { LPCommitment } from '@/types'

export function LPCommitmentsPage() {
  const [commitments, setCommitments] = useState<LPCommitment[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/lp-commitments')
      .then(({ data }) => setCommitments(data))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <h2 className="text-lg font-semibold mb-6">LP Commitments</h2>
      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>
        ) : commitments.length === 0 ? (
          <div className="flex items-center justify-center h-64 text-gray-400">No LP commitments</div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-800">
                <th className="text-left py-3 px-4 font-medium text-gray-500">Fund</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Amount ($M)</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Status</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Date</th>
              </tr>
            </thead>
            <tbody>
              {commitments.map((c) => (
                <tr key={c.id} className="border-b border-gray-100 dark:border-gray-800/50">
                  <td className="py-3 px-4 font-medium">{c.fund_vehicle_id}</td>
                  <td className="py-3 px-4 text-gray-500">
                    {c.commitment_amount_mm ? `$${c.commitment_amount_mm}` : '—'}
                  </td>
                  <td className="py-3 px-4">
                    {c.status && (
                      <span className={`px-2 py-0.5 rounded-full text-xs ${
                        c.status === 'committed'
                          ? 'bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400'
                          : c.status === 'considering'
                          ? 'bg-amber-100 dark:bg-amber-900/20 text-amber-700'
                          : 'bg-gray-100 dark:bg-gray-800 text-gray-600'
                      }`}>
                        {c.status}
                      </span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-gray-500 text-xs">
                    {c.commitment_date ? formatDate(c.commitment_date) : '—'}
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
