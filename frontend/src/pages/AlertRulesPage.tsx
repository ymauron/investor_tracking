import { useState, useEffect } from 'react'
import { Plus, Trash2, Pencil } from 'lucide-react'
import { listAlertRules, createAlertRule, updateAlertRule, deleteAlertRule } from '@/api/alerts'
import { formatArea } from '@/lib/utils'
import type { AlertRule } from '@/types'

const emptyRule = {
  name: '',
  therapeutic_area: '',
  transaction_type: '',
  keyword: '',
  company_name: '',
  is_active: true,
}

export function AlertRulesPage() {
  const [rules, setRules] = useState<AlertRule[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [form, setForm] = useState(emptyRule)

  const load = () => {
    listAlertRules()
      .then(setRules)
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const handleSubmit = async () => {
    const payload = {
      name: form.name,
      therapeutic_area: form.therapeutic_area || null,
      transaction_type: form.transaction_type || null,
      keyword: form.keyword || null,
      company_name: form.company_name || null,
      is_active: form.is_active,
    }

    if (editingId) {
      await updateAlertRule(editingId, payload)
    } else {
      await createAlertRule(payload)
    }
    setShowForm(false)
    setEditingId(null)
    setForm(emptyRule)
    load()
  }

  const handleEdit = (rule: AlertRule) => {
    setForm({
      name: rule.name,
      therapeutic_area: rule.therapeutic_area || '',
      transaction_type: rule.transaction_type || '',
      keyword: rule.keyword || '',
      company_name: rule.company_name || '',
      is_active: rule.is_active,
    })
    setEditingId(rule.id)
    setShowForm(true)
  }

  const handleDelete = async (id: string) => {
    await deleteAlertRule(id)
    load()
  }

  const handleToggle = async (rule: AlertRule) => {
    await updateAlertRule(rule.id, { is_active: !rule.is_active })
    load()
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold">Alert Rules</h2>
        <button
          onClick={() => { setShowForm(true); setEditingId(null); setForm(emptyRule) }}
          className="flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-lg bg-brand-600 text-white hover:bg-brand-700"
        >
          <Plus size={14} /> New Rule
        </button>
      </div>

      {showForm && (
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-4 mb-6">
          <h3 className="text-sm font-semibold mb-4">{editingId ? 'Edit Rule' : 'New Alert Rule'}</h3>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-xs text-gray-500 mb-1">Name *</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm(f => ({ ...f, name: e.target.value }))}
                className="w-full px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                placeholder="e.g. Oncology M&A alerts"
              />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Company Name</label>
              <input
                type="text"
                value={form.company_name}
                onChange={(e) => setForm(f => ({ ...f, company_name: e.target.value }))}
                className="w-full px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                placeholder="e.g. Pfizer"
              />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Transaction Type</label>
              <select
                value={form.transaction_type}
                onChange={(e) => setForm(f => ({ ...f, transaction_type: e.target.value }))}
                className="w-full px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
              >
                <option value="">Any</option>
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
                value={form.therapeutic_area}
                onChange={(e) => setForm(f => ({ ...f, therapeutic_area: e.target.value }))}
                className="w-full px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
              >
                <option value="">Any</option>
                <option value="oncology">Oncology</option>
                <option value="rare_disease">Rare Disease</option>
                <option value="neurology">Neurology</option>
                <option value="immunology">Immunology</option>
                <option value="cardiology">Cardiology</option>
                <option value="infectious_disease">Infectious Disease</option>
                <option value="gene_therapy">Gene Therapy</option>
                <option value="digital_health">Digital Health</option>
                <option value="medical_device">Medical Device</option>
              </select>
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Keyword</label>
              <input
                type="text"
                value={form.keyword}
                onChange={(e) => setForm(f => ({ ...f, keyword: e.target.value }))}
                className="w-full px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                placeholder="e.g. CAR-T"
              />
            </div>
          </div>
          <div className="flex gap-3">
            <button
              onClick={handleSubmit}
              disabled={!form.name}
              className="px-4 py-2 text-sm rounded-lg bg-brand-600 text-white hover:bg-brand-700 disabled:opacity-50"
            >
              {editingId ? 'Update' : 'Create'}
            </button>
            <button
              onClick={() => { setShowForm(false); setEditingId(null); setForm(emptyRule) }}
              className="px-4 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>
        ) : rules.length === 0 ? (
          <div className="flex items-center justify-center h-64 text-gray-400">No alert rules configured</div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-800">
                <th className="text-left py-3 px-4 font-medium text-gray-500">Name</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Type</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Area</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Keyword</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Company</th>
                <th className="text-left py-3 px-4 font-medium text-gray-500">Active</th>
                <th className="text-right py-3 px-4 font-medium text-gray-500">Actions</th>
              </tr>
            </thead>
            <tbody>
              {rules.map((rule) => (
                <tr key={rule.id} className="border-b border-gray-100 dark:border-gray-800/50">
                  <td className="py-3 px-4 font-medium">{rule.name}</td>
                  <td className="py-3 px-4 text-gray-500">{rule.transaction_type ? rule.transaction_type.replace(/_/g, ' ') : 'Any'}</td>
                  <td className="py-3 px-4 text-gray-500">{formatArea(rule.therapeutic_area) || 'Any'}</td>
                  <td className="py-3 px-4 text-gray-500">{rule.keyword || '—'}</td>
                  <td className="py-3 px-4 text-gray-500">{rule.company_name || '—'}</td>
                  <td className="py-3 px-4">
                    <button
                      onClick={() => handleToggle(rule)}
                      className={`w-8 h-5 rounded-full relative transition-colors ${rule.is_active ? 'bg-brand-600' : 'bg-gray-300 dark:bg-gray-600'}`}
                    >
                      <span className={`absolute top-0.5 w-4 h-4 rounded-full bg-white transition-transform ${rule.is_active ? 'left-3.5' : 'left-0.5'}`} />
                    </button>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <button onClick={() => handleEdit(rule)} className="p-1 text-gray-400 hover:text-gray-600">
                        <Pencil size={14} />
                      </button>
                      <button onClick={() => handleDelete(rule.id)} className="p-1 text-gray-400 hover:text-red-600">
                        <Trash2 size={14} />
                      </button>
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
