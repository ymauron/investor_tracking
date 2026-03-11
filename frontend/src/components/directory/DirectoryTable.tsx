import { useNavigate } from 'react-router-dom'
import { formatArea, formatDate } from '@/lib/utils'
import type { IndividualListItem } from '@/types'

interface Props {
  individuals: IndividualListItem[]
  loading: boolean
}

export function DirectoryTable({ individuals, loading }: Props) {
  const navigate = useNavigate()

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400">
        Loading...
      </div>
    )
  }

  if (individuals.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400">
        No individuals found
      </div>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-200 dark:border-gray-800">
            <th className="text-left py-3 px-4 font-medium text-gray-500">Name</th>
            <th className="text-left py-3 px-4 font-medium text-gray-500">Therapeutic Area</th>
            <th className="text-left py-3 px-4 font-medium text-gray-500">Relationship</th>
            <th className="text-left py-3 px-4 font-medium text-gray-500">Added</th>
          </tr>
        </thead>
        <tbody>
          {individuals.map((ind) => (
            <tr
              key={ind.id}
              onClick={() => navigate(`/individuals/${ind.id}`)}
              className="border-b border-gray-100 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-900 cursor-pointer transition-colors"
            >
              <td className="py-3 px-4 font-medium">
                {ind.first_name} {ind.last_name}
              </td>
              <td className="py-3 px-4 text-gray-600 dark:text-gray-400">
                {formatArea(ind.primary_therapeutic_area)}
              </td>
              <td className="py-3 px-4">
                {ind.relationship_status && (
                  <span className="inline-flex px-2 py-0.5 rounded-full text-xs bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400">
                    {ind.relationship_status}
                  </span>
                )}
              </td>
              <td className="py-3 px-4 text-gray-500 text-xs">
                {formatDate(ind.created_at)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
