import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, ExternalLink } from 'lucide-react'
import { getTransaction, updateTransaction } from '@/api/transactions'
import { formatDate, formatArea } from '@/lib/utils'
import type { Transaction } from '@/types'

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

export function TransactionDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [txn, setTxn] = useState<Transaction | null>(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [editType, setEditType] = useState('')
  const [editArea, setEditArea] = useState('')

  useEffect(() => {
    if (!id) return
    getTransaction(id)
      .then((t) => {
        setTxn(t)
        setEditType(t.transaction_type || '')
        setEditArea(t.therapeutic_area || '')
      })
      .finally(() => setLoading(false))
  }, [id])

  const handleSave = async () => {
    if (!id) return
    const updates: Record<string, unknown> = {}
    if (editType !== (txn?.transaction_type || '')) updates.transaction_type = editType || null
    if (editArea !== (txn?.therapeutic_area || '')) updates.therapeutic_area = editArea || null
    if (Object.keys(updates).length > 0) {
      const updated = await updateTransaction(id, updates)
      setTxn(updated)
    }
    setEditing(false)
  }

  if (loading) {
    return <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>
  }

  if (!txn) {
    return <div className="flex items-center justify-center h-64 text-gray-400">Transaction not found</div>
  }

  return (
    <div>
      <button
        onClick={() => navigate('/transactions')}
        className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-700 mb-4"
      >
        <ArrowLeft size={14} /> Back to Transactions
      </button>

      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h2 className="text-lg font-semibold mb-2">{txn.title}</h2>
            <div className="flex items-center gap-3 text-sm text-gray-500">
              <span>{formatDate(txn.published_at)}</span>
              <span className="px-2 py-0.5 rounded-full text-xs bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">
                {txn.source.replace(/_/g, ' ')}
              </span>
              {txn.transaction_type && (
                <span className={`px-2 py-0.5 rounded-full text-xs ${TYPE_COLORS[txn.transaction_type] || TYPE_COLORS.other}`}>
                  {txn.transaction_type.replace(/_/g, ' ')}
                </span>
              )}
            </div>
          </div>
          <a
            href={txn.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800"
          >
            <ExternalLink size={14} /> Source
          </a>
        </div>

        <div className="grid grid-cols-2 gap-6 mb-6">
          <div>
            <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Details</h3>
            <dl className="space-y-2 text-sm">
              <div className="flex justify-between">
                <dt className="text-gray-500">Therapeutic Area</dt>
                <dd>{formatArea(txn.therapeutic_area) || '—'}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Clinical Stage</dt>
                <dd>{txn.stage ? txn.stage.replace(/_/g, ' ') : '—'}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Deal Value</dt>
                <dd>{txn.deal_value_mm ? `$${txn.deal_value_mm}M` : '—'}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Sentiment</dt>
                <dd>{txn.sentiment || '—'}</dd>
              </div>
            </dl>
          </div>
          <div>
            <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Linked Entities</h3>
            <dl className="space-y-2 text-sm">
              <div className="flex justify-between">
                <dt className="text-gray-500">Portfolio Company</dt>
                <dd>
                  {txn.portfolio_company_name ? (
                    <button onClick={() => navigate(`/firms/${txn.portfolio_company_id}`)} className="text-brand-600 hover:underline">
                      {txn.portfolio_company_name}
                    </button>
                  ) : '—'}
                </dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Management Company</dt>
                <dd>
                  {txn.management_company_name ? (
                    <button onClick={() => navigate(`/firms/${txn.management_company_id}`)} className="text-brand-600 hover:underline">
                      {txn.management_company_name}
                    </button>
                  ) : '—'}
                </dd>
              </div>
            </dl>
          </div>
        </div>

        {txn.companies_mentioned && txn.companies_mentioned.length > 0 && (
          <div className="mb-6">
            <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Companies Mentioned</h3>
            <div className="flex flex-wrap gap-2">
              {txn.companies_mentioned.map((c, i) => (
                <span key={i} className="px-2 py-1 text-xs rounded-lg bg-gray-100 dark:bg-gray-800">
                  {c}
                </span>
              ))}
            </div>
          </div>
        )}

        {txn.summary && (
          <div className="mb-6">
            <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Summary</h3>
            <p className="text-sm text-gray-700 dark:text-gray-300">{txn.summary}</p>
          </div>
        )}

        {txn.raw_description && (
          <div>
            <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Raw Description</h3>
            <p className="text-sm text-gray-500">{txn.raw_description}</p>
          </div>
        )}

        <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-800">
          {!editing ? (
            <button
              onClick={() => setEditing(true)}
              className="px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
              Edit Classification
            </button>
          ) : (
            <div className="flex items-end gap-4">
              <div>
                <label className="block text-xs text-gray-500 mb-1">Type</label>
                <select
                  value={editType}
                  onChange={(e) => setEditType(e.target.value)}
                  className="px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                >
                  <option value="">Unknown</option>
                  <option value="ma">M&A</option>
                  <option value="ipo">IPO</option>
                  <option value="licensing">Licensing</option>
                  <option value="funding_round">Funding Round</option>
                  <option value="partnership">Partnership</option>
                </select>
              </div>
              <div>
                <label className="block text-xs text-gray-500 mb-1">Therapeutic Area</label>
                <select
                  value={editArea}
                  onChange={(e) => setEditArea(e.target.value)}
                  className="px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                >
                  <option value="">Unknown</option>
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
              <button
                onClick={handleSave}
                className="px-3 py-2 text-sm rounded-lg bg-brand-600 text-white hover:bg-brand-700"
              >
                Save
              </button>
              <button
                onClick={() => setEditing(false)}
                className="px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800"
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
