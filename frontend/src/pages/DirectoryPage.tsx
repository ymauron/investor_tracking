import { useState, useEffect } from 'react'
import { Search } from 'lucide-react'
import { useDebounce } from '@/hooks/useDebounce'
import { listIndividuals } from '@/api/individuals'
import { DirectoryTable } from '@/components/directory/DirectoryTable'
import { THERAPEUTIC_AREAS } from '@/lib/constants'
import type { IndividualListItem } from '@/types'

export function DirectoryPage() {
  const [individuals, setIndividuals] = useState<IndividualListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [areaFilter, setAreaFilter] = useState('')
  const debouncedSearch = useDebounce(searchQuery, 300)

  useEffect(() => {
    setLoading(true)
    listIndividuals({
      search: debouncedSearch || undefined,
      therapeutic_area: areaFilter || undefined,
    })
      .then(setIndividuals)
      .finally(() => setLoading(false))
  }, [debouncedSearch, areaFilter])

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">People Directory</h2>
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
            value={areaFilter}
            onChange={(e) => setAreaFilter(e.target.value)}
            className="px-3 py-1.5 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-brand-500"
          >
            <option value="">All Areas</option>
            {THERAPEUTIC_AREAS.map((a) => (
              <option key={a.value} value={a.value}>{a.label}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
        <DirectoryTable individuals={individuals} loading={loading} />
      </div>
    </div>
  )
}
