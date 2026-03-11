import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { getFirm, getFirmPeople, getFirmFunds, getFirmPortfolio } from '@/api/firms'
import { formatArea } from '@/lib/utils'
import type { ManagementCompany, IndividualListItem, FundVehicle, PortfolioCompany } from '@/types'

export function FirmPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [firm, setFirm] = useState<ManagementCompany | null>(null)
  const [people, setPeople] = useState<IndividualListItem[]>([])
  const [funds, setFunds] = useState<FundVehicle[]>([])
  const [portfolio, setPortfolio] = useState<PortfolioCompany[]>([])
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState<'people' | 'funds' | 'portfolio'>('people')

  useEffect(() => {
    if (!id) return
    setLoading(true)
    Promise.all([
      getFirm(id),
      getFirmPeople(id, false),
      getFirmFunds(id),
      getFirmPortfolio(id),
    ]).then(([f, p, fv, pc]) => {
      setFirm(f)
      setPeople(p)
      setFunds(fv)
      setPortfolio(pc)
    }).finally(() => setLoading(false))
  }, [id])

  if (loading || !firm) {
    return <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>
  }

  return (
    <div className="max-w-4xl">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-700 mb-4">
        <ArrowLeft size={14} /> Back
      </button>

      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 mb-4">
        <h2 className="text-xl font-bold">{firm.name}</h2>
        <div className="flex items-center gap-2 mt-1">
          <span className="px-2.5 py-0.5 rounded-full text-xs bg-brand-50 dark:bg-brand-900/20 text-brand-700 dark:text-brand-300">
            {firm.firm_type.replace(/_/g, ' ').toUpperCase()}
          </span>
          {firm.hq_city && firm.hq_state && (
            <span className="text-sm text-gray-500">{firm.hq_city}, {firm.hq_state}</span>
          )}
        </div>
        {firm.description && <p className="mt-3 text-sm text-gray-600 dark:text-gray-400">{firm.description}</p>}
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
        <div className="flex border-b border-gray-200 dark:border-gray-800">
          {(['people', 'funds', 'portfolio'] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-3 text-sm font-medium transition-colors ${
                tab === t
                  ? 'border-b-2 border-brand-600 text-brand-700 dark:text-brand-300'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {t === 'people' ? `People (${people.length})` : t === 'funds' ? `Funds (${funds.length})` : `Portfolio (${portfolio.length})`}
            </button>
          ))}
        </div>

        <div className="p-4">
          {tab === 'people' && (
            <div className="space-y-2">
              {people.map((p) => (
                <Link
                  key={p.id}
                  to={`/individuals/${p.id}`}
                  className="block p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                >
                  <span className="text-sm font-medium">{p.first_name} {p.last_name}</span>
                  {p.primary_therapeutic_area && (
                    <span className="ml-2 text-xs text-gray-500">{formatArea(p.primary_therapeutic_area)}</span>
                  )}
                </Link>
              ))}
              {people.length === 0 && <p className="text-sm text-gray-400">No people recorded</p>}
            </div>
          )}

          {tab === 'funds' && (
            <div className="space-y-2">
              {funds.map((f) => (
                <div key={f.id} className="p-3 rounded-lg bg-gray-50 dark:bg-gray-800">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">{f.name}</span>
                    <span className="text-xs text-gray-500">
                      {f.vintage_year && `Vintage ${f.vintage_year}`}
                      {f.target_size_mm && ` | $${f.target_size_mm}M target`}
                    </span>
                  </div>
                  {f.status && (
                    <span className="inline-flex mt-1 px-2 py-0.5 rounded text-xs bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400">
                      {f.status}
                    </span>
                  )}
                </div>
              ))}
              {funds.length === 0 && <p className="text-sm text-gray-400">No funds recorded</p>}
            </div>
          )}

          {tab === 'portfolio' && (
            <div className="space-y-2">
              {portfolio.map((pc) => (
                <div key={pc.id} className="p-3 rounded-lg bg-gray-50 dark:bg-gray-800">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">{pc.name}</span>
                    <div className="flex gap-2">
                      {pc.therapeutic_area && (
                        <span className="text-xs text-gray-500">{formatArea(pc.therapeutic_area)}</span>
                      )}
                      {pc.stage && (
                        <span className="px-2 py-0.5 rounded text-xs bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400">
                          {pc.stage.replace(/_/g, ' ')}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              {portfolio.length === 0 && <p className="text-sm text-gray-400">No portfolio companies recorded</p>}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
