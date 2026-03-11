import { useState, useRef, useEffect } from 'react'
import { Search, X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useDebounce } from '@/hooks/useDebounce'
import { search } from '@/api/graph'
import type { SearchResults, SearchResult } from '@/types'

export function SearchBar() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResults | null>(null)
  const [open, setOpen] = useState(false)
  const debouncedQuery = useDebounce(query, 300)
  const navigate = useNavigate()
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (debouncedQuery.length >= 2) {
      search(debouncedQuery).then(setResults)
      setOpen(true)
    } else {
      setResults(null)
      setOpen(false)
    }
  }, [debouncedQuery])

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSelect = (item: SearchResult) => {
    setOpen(false)
    setQuery('')
    if (item.type === 'individual') navigate(`/individuals/${item.id}`)
    else if (item.type === 'firm') navigate(`/firms/${item.id}`)
    else if (item.type === 'deal') navigate(`/deals/${item.id}`)
  }

  const allResults = results
    ? [...results.individuals, ...results.firms, ...results.deals]
    : []

  return (
    <div ref={ref} className="relative w-full max-w-md">
      <div className="relative">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => allResults.length > 0 && setOpen(true)}
          placeholder="Search people, firms, deals..."
          className="w-full pl-9 pr-8 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
        />
        {query && (
          <button
            onClick={() => { setQuery(''); setOpen(false) }}
            className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
          >
            <X size={14} />
          </button>
        )}
      </div>

      {open && allResults.length > 0 && (
        <div className="absolute top-full mt-1 w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50 max-h-80 overflow-y-auto">
          {results!.individuals.length > 0 && (
            <div>
              <div className="px-3 py-1.5 text-xs font-semibold text-gray-500 uppercase">People</div>
              {results!.individuals.map((r) => (
                <button
                  key={r.id}
                  onClick={() => handleSelect(r)}
                  className="w-full px-3 py-2 text-left text-sm hover:bg-gray-50 dark:hover:bg-gray-800 flex justify-between"
                >
                  <span>{r.name}</span>
                  {r.detail && <span className="text-xs text-gray-400">{r.detail}</span>}
                </button>
              ))}
            </div>
          )}
          {results!.firms.length > 0 && (
            <div>
              <div className="px-3 py-1.5 text-xs font-semibold text-gray-500 uppercase">Firms</div>
              {results!.firms.map((r) => (
                <button
                  key={r.id}
                  onClick={() => handleSelect(r)}
                  className="w-full px-3 py-2 text-left text-sm hover:bg-gray-50 dark:hover:bg-gray-800 flex justify-between"
                >
                  <span>{r.name}</span>
                  {r.detail && <span className="text-xs text-gray-400">{r.detail}</span>}
                </button>
              ))}
            </div>
          )}
          {results!.deals.length > 0 && (
            <div>
              <div className="px-3 py-1.5 text-xs font-semibold text-gray-500 uppercase">Deals</div>
              {results!.deals.map((r) => (
                <button
                  key={r.id}
                  onClick={() => handleSelect(r)}
                  className="w-full px-3 py-2 text-left text-sm hover:bg-gray-50 dark:hover:bg-gray-800 flex justify-between"
                >
                  <span>{r.name}</span>
                  {r.detail && <span className="text-xs text-gray-400">{r.detail}</span>}
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
