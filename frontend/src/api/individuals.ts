import api from './client'
import type { Individual, IndividualListItem, Role, MovementEvent, Note } from '@/types'

export async function listIndividuals(params?: {
  search?: string
  therapeutic_area?: string
  page?: number
  per_page?: number
}): Promise<IndividualListItem[]> {
  const { data } = await api.get('/individuals', { params })
  return data
}

export async function getIndividual(id: string): Promise<Individual> {
  const { data } = await api.get(`/individuals/${id}`)
  return data
}

export async function getIndividualRoles(id: string): Promise<Role[]> {
  const { data } = await api.get(`/individuals/${id}/roles`)
  return data
}

export async function getIndividualMovements(id: string): Promise<MovementEvent[]> {
  const { data } = await api.get(`/individuals/${id}/movements`)
  return data
}

export async function getIndividualNotes(id: string): Promise<Note[]> {
  const { data } = await api.get(`/individuals/${id}/notes`)
  return data
}
