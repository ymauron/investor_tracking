import api from './client'
import type { TransactionListResponse, Transaction, CrawlStats, TransactionStats } from '@/types'

export async function listTransactions(params?: {
  transaction_type?: string
  source?: string
  therapeutic_area?: string
  stage?: string
  from_date?: string
  to_date?: string
  search?: string
  linked_only?: boolean
  page?: number
  per_page?: number
}): Promise<TransactionListResponse> {
  const { data } = await api.get('/transactions', { params })
  return data
}

export async function getTransaction(id: string): Promise<Transaction> {
  const { data } = await api.get(`/transactions/${id}`)
  return data
}

export async function updateTransaction(id: string, updates: Record<string, unknown>): Promise<Transaction> {
  const { data } = await api.put(`/transactions/${id}`, updates)
  return data
}

export async function deleteTransaction(id: string): Promise<void> {
  await api.delete(`/transactions/${id}`)
}

export async function triggerCrawl(): Promise<CrawlStats> {
  const { data } = await api.post('/transactions/crawl')
  return data
}

export async function getTransactionStats(): Promise<TransactionStats> {
  const { data } = await api.get('/transactions/stats')
  return data
}
