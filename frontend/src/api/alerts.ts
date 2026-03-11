import api from './client'
import type { AlertRule, AlertNotification } from '@/types'

export async function listAlertRules(): Promise<AlertRule[]> {
  const { data } = await api.get('/alerts/rules')
  return data
}

export async function createAlertRule(rule: Omit<AlertRule, 'id' | 'created_at' | 'updated_at'>): Promise<AlertRule> {
  const { data } = await api.post('/alerts/rules', rule)
  return data
}

export async function updateAlertRule(id: string, updates: Record<string, unknown>): Promise<AlertRule> {
  const { data } = await api.put(`/alerts/rules/${id}`, updates)
  return data
}

export async function deleteAlertRule(id: string): Promise<void> {
  await api.delete(`/alerts/rules/${id}`)
}

export async function listNotifications(params?: {
  unread_only?: boolean
  page?: number
  per_page?: number
}): Promise<AlertNotification[]> {
  const { data } = await api.get('/alerts/notifications', { params })
  return data
}

export async function getUnreadCount(): Promise<number> {
  const { data } = await api.get('/alerts/notifications/count')
  return data.count
}

export async function markAsRead(id: string): Promise<void> {
  await api.put(`/alerts/notifications/${id}/read`)
}

export async function markAllAsRead(): Promise<void> {
  await api.put('/alerts/notifications/read-all')
}
