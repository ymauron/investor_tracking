import { FIRM_TYPES, THERAPEUTIC_AREAS } from '@/lib/constants'

interface Filters {
  firmType: string
  therapeuticArea: string
  lpCommittedOnly: boolean
}

interface Props {
  filters: Filters
  onChange: (filters: Filters) => void
}

export function GraphControls({ filters, onChange }: Props) {
  return (
    <div className="flex items-center gap-3 flex-wrap">
      <select
        value={filters.firmType}
        onChange={(e) => onChange({ ...filters, firmType: e.target.value })}
        className="px-3 py-1.5 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-brand-500"
      >
        <option value="">All Firm Types</option>
        {FIRM_TYPES.map((t) => (
          <option key={t.value} value={t.value}>{t.label}</option>
        ))}
      </select>

      <select
        value={filters.therapeuticArea}
        onChange={(e) => onChange({ ...filters, therapeuticArea: e.target.value })}
        className="px-3 py-1.5 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-brand-500"
      >
        <option value="">All Therapeutic Areas</option>
        {THERAPEUTIC_AREAS.map((a) => (
          <option key={a.value} value={a.value}>{a.label}</option>
        ))}
      </select>

      <label className="flex items-center gap-2 text-sm cursor-pointer">
        <input
          type="checkbox"
          checked={filters.lpCommittedOnly}
          onChange={(e) => onChange({ ...filters, lpCommittedOnly: e.target.checked })}
          className="rounded border-gray-300 text-brand-600 focus:ring-brand-500"
        />
        LP Committed Only
      </label>
    </div>
  )
}
