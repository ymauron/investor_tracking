import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { RefreshCw, ExternalLink } from 'lucide-react'
import { listTransactions, triggerCrawl, getTransactionStats } from '@/api/transactions'
import { formatDate, formatArea } from '@/lib/utils'
import type { Transaction, TransactionListResponse, TransactionStats, CrawlStats } from '@/types'

const TYPE_COLORS: Record<string, string> = {
  ma: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
  ipo: 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400',
  funding_round: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400',
  fda_approval: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
  fda_rejection: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
  clinical_trial: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400',
  licensing: 'bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-400',
  partnership: 'bg-violet-100 text-violet-700 dark:bg-violet-900/30 dark:text-violet-400',
  bankruptcy: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400',
  other: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
}

const SOURCE_COLORS: Record<string, string> = {
  biospace: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
  fierce_biotech: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
  fierce_pharma: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
}

export function TransactionsPage() {
  const navigate = useNavigate()
  const [data, setData] = useState<TransactionListResponse | null>(null)
  const [stats, setStats] = useState<TransactionStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [crawling, setCrawling] = useState(false)
  const [crawlResult, setCrawlResult] = useState<CrawlStats | null>(null)
  const [page, setPage] = useState(1)
  const [filters, setFilters] = useState({
    transaction_type: '',
    source: '',
    therapeutic_area: '',
    search: '',
  })

  const perPage = 50

  const load = () => {
    setLoading(true)
    const params: Record<string, unknown> = { page, per_page: perPage }
    if (filters.transaction_type) params.transaction_type = filters.transaction_type
    if (filters.source) params.source = filters.source
    if (filters.therapeutic_area) params.therapeutic_area = filters.therapeutic_area
    if (filters.search) params.search = filters.search

    listTransactions(params as Parameters<typeof listTransactions>[0])
      .then(setData)
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [page, filters])
  useEffect(() => { getTransactionStats().then(setStats) }, [])

  const handleCrawl = async () => {
    setCrawling(true)
    setCrawlResult(null)
    try {
      const result = await triggerCrawl()
      setCrawlResult(result)
      load()
      getTransactionStats().then(setStats)
    } finally {
      setCrawling(false)
    }
  }

  const totalPages = data ? Math.ceil(data.total / perPage) : 0

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Transactions</h2>
        <button
          onClick={handleCrawl}
          disabled={crawling}
          className="flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-lg bg-brand-600 text-white hover:bg-brand-700 disabled:opacity-50"
        >
          <RefreshCw size={14} className={crawling ? 'animate-spin' : ''} />
          {crawling ? 'Crawling...' : 'Run Crawl'}
        </button>
      </div>

      {crawlResult && (
        <div className="mb-4 px-4 py-2 rounded-lg bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 text-sm">
          Crawl complete: {crawlResult.new} new, {crawlResult.skipped} skipped, {crawlResult.errors} errors
        </div>
      )}

      {stats && (
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-4">
            <div className="text-2xl font-bold">{stats.total}</div>
            <div className="text-xs text-gray-500">Total</div>
          </div>
          <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-4">
            <div className="text-2xl font-bold">{stats.this_week}</div>
            <div className="text-xs text-gray-500">This Week</div>
          </div>
          <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-4">
            <div className="text-2xl font-bold">{stats.this_month}</div>
            <div className="text-xs text-gray-500">This Month</div>
          </div>
          <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-4">
            <div className="text-2xl font-bold">{Object.keys(stats.by_source).length}</div>
            <div className="text-xs text-gray-500">Sources</div>
          </div>
        </div>
      )}

      <div className="flex gap-3 mb-4 flex-wrap">
        <input
          type="text"
          placeholder="Search transactions..."
          value={filters.search}
          onChange={(e) => { setFilters(f => ({ ...f, search: e.target.value })); setPage(1) }}
          className="px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-brand-500 w-64"
        />
        <select
          value={filters.transaction_type}
          onChange={(e) => { setFilters(f => ({ ...f, transaction_type: e.target.value })); setPage(1) }}
          className="px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
        >
          <option value="">All Types</option>
          <option value="ma">M&A</option>
          <option value="ipo">IPO</option>
          <option value="licensing">Licensing</option>
          <option value="clinical_trial">Clinical Trial</option>
          <option value="fda_approval">FDA Approval</option>
          <option value="fda_rejection">FDA Rejection</option>
          <option value="funding_round">Funding Round</option>
          <option value="partnership">Partnership</option>
          <option value="bankruptcy">Bankruptcy</option>
          <option value="other">Other</option>
        </select>
        <select
          value={filters.source}
          onChange={(e) => { setFilters(f => ({ ...f, source: e.target.value })); setPage(1) }}
          className="px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
        >
          <option value="">All Sources</option>
          <option value="biospace">BioSpace</option>
          <option value="fierce_biotech">Fierce Biotech</option>
          <option value="fierce_pharma">Fierce Pharma</option>
        </select>
        <select
          value={filters.therapeutic_area}
          onChange={(e) => { setFilters(f => ({ ...f, therapeutic_area: e.target.value })); setPage(1) }}
          className="px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
        >
          <option value="">All Areas</option>
          <option value="oncology">Oncology</option>
          <option value="rare_disease">Rare Disease</option>
          <option value="neurology">Neurology</option>
          <option value="immunology">Immunology</option>
          <option value="cardiology">Cardiology</option>
          <option value="infectious_disease">Infectious Disease</option>
          <option value="gene_therapy">Gene Therapy</option>
          <option value="digital_health">Digital Health</option>
          <option value="medical_device">Medical Device</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>
        ) : !data || data.items.length === 0 ? (
          <div className="flex items-center justify-center h-64 text-gray-400">No transactions found</div>
        ) : (
          <>
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-800">
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Title</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Type</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Source</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Area</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Value</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Date</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500 w-8"></th>
                </tr>
              </thead>
              <tbody>
                {data.items.map((t) => (
                  <tr
                    key={t.id}
                    onClick={() => navigate(`/transactions/${t.id}`)}
                    className="border-b border-gray-100 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-800/50 cursor-pointer"
                  >
                    <td className="py-3 px-4 font-medium max-w-xs truncate">{t.title}</td>
                    <td className="py-3 px-4">
                      {t.transaction_type && (
                        <span className={`px-2 py-0.5 rounded-full text-xs ${TYPE_COLORS[t.transaction_type] || TYPE_COLORS.other}`}>
                          {t.transaction_type.replace(/_/g, ' ')}
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded-full text-xs ${SOURCE_COLORS[t.source] || ''}`}>
                        {t.source.replace(/_/g, ' ')}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-gray-500">{formatArea(t.therapeutic_area)}</td>
                    <td className="py-3 px-4 text-gray-500">{t.deal_value_mm ? `$${t.deal_value_mm}M` : ''}</td>
                    <td className="py-3 px-4 text-gray-500 text-xs">{formatDate(t.published_at)}</td>
                    <td className="py-3 px-4">
                      <a
                        href={t.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className="text-gray-400 hover:text-brand-600"
                      >
                        <ExternalLink size={14} />
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {totalPages > 1 && (
              <div className="flex items-center justify-between px-4 py-3 border-t border-gray-200 dark:border-gray-800">
                <span className="text-xs text-gray-500">{data.total} results</span>
                <div className="flex gap-2">
                  <button
                    onClick={() => setPage(p => Math.max(1, p - 1))}
                    disabled={page === 1}
                    className="px-3 py-1 text-xs rounded border border-gray-200 dark:border-gray-700 disabled:opacity-40"
                  >
                    Previous
                  </button>
                  <span className="px-3 py-1 text-xs text-gray-500">{page} / {totalPages}</span>
                  <button
                    onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                    disabled={page === totalPages}
                    className="px-3 py-1 text-xs rounded border border-gray-200 dark:border-gray-700 disabled:opacity-40"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
