export const THERAPEUTIC_AREAS = [
  { value: 'oncology', label: 'Oncology' },
  { value: 'rare_disease', label: 'Rare Disease' },
  { value: 'medtech', label: 'MedTech' },
  { value: 'digital_health', label: 'Digital Health' },
  { value: 'neuroscience', label: 'Neuroscience' },
  { value: 'immunology', label: 'Immunology' },
  { value: 'cardiovascular', label: 'Cardiovascular' },
  { value: 'gene_therapy', label: 'Gene Therapy' },
  { value: 'diagnostics', label: 'Diagnostics' },
  { value: 'multi_sector', label: 'Multi-Sector' },
  { value: 'other', label: 'Other' },
]

export const FIRM_TYPES = [
  { value: 'vc', label: 'VC' },
  { value: 'growth_equity', label: 'Growth Equity' },
  { value: 'buyout', label: 'Buyout' },
  { value: 'crossover', label: 'Crossover' },
  { value: 'corporate_vc', label: 'Corporate VC' },
  { value: 'family_office', label: 'Family Office' },
  { value: 'other', label: 'Other' },
]

export const NODE_COLORS: Record<string, string> = {
  vc: '#3b82f6',
  growth_equity: '#10b981',
  buyout: '#f59e0b',
  crossover: '#8b5cf6',
  corporate_vc: '#ec4899',
  family_office: '#6366f1',
  person: '#6b7280',
  lp_committed: '#ef4444',
  other: '#9ca3af',
}
