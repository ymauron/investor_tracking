import api from './client'
import type { ManagementCompany, FundVehicle, PortfolioCompany, IndividualListItem } from '@/types'

export async function listFirms(params?: {
  search?: string
  firm_type?: string
}): Promise<ManagementCompany[]> {
  const { data } = await api.get('/firms', { params })
  return data
}

export async function getFirm(id: string): Promise<ManagementCompany> {
  const { data } = await api.get(`/firms/${id}`)
  return data
}

export async function getFirmPeople(id: string, currentOnly = true): Promise<IndividualListItem[]> {
  const { data } = await api.get(`/firms/${id}/people`, { params: { current_only: currentOnly } })
  return data
}

export async function getFirmFunds(id: string): Promise<FundVehicle[]> {
  const { data } = await api.get(`/firms/${id}/funds`)
  return data
}

export async function getFirmPortfolio(id: string): Promise<PortfolioCompany[]> {
  const { data } = await api.get(`/firms/${id}/portfolio`)
  return data
}
