import api from './client'
import type { GraphData, TimelineEvent } from '@/types'

export async function getNetworkGraph(params?: {
  firm_type?: string
  therapeutic_area?: string
  from_date?: string
  to_date?: string
  lp_committed_only?: boolean
}): Promise<GraphData> {
  const { data } = await api.get('/graph/network', { params })
  return data
}

export async function getTimeline(params?: {
  from_date?: string
  to_date?: string
}): Promise<{ events: TimelineEvent[] }> {
  const { data } = await api.get('/graph/timeline', { params })
  return data
}

export async function search(q: string) {
  const { data } = await api.get('/search', { params: { q } })
  return data
}
