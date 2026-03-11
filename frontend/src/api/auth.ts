import api from './client'

export async function login(username: string, password: string): Promise<string> {
  const { data } = await api.post('/auth/login', { username, password })
  return data.access_token
}

export async function getMe() {
  const { data } = await api.get('/auth/me')
  return data
}
