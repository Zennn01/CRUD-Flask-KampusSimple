const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:5000'

export type ApiClass = { id_kelas: number; nama_kelas: string }
export type ApiCourse = { id_matakuliah: number; nama_matakuliah: string; sks: number; nama_kelas?: string; nama_dosen?: string }
export type ApiStudent = { id_mahasiswa: number; nama: string; nim: string; semester: number; id_kelas: number }

export function getToken() {
  return localStorage.getItem('ruangkampus_token')
}

export type LoginResponse = { message: string; token: string }

export async function login(username: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  const body = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(body.message ?? 'Login gagal')
  localStorage.setItem('ruangkampus_token', body.token)
  return body as LoginResponse
}

export function getTokenPayload() {
  const token = getToken()
  if (!token) return null
  try {
    return JSON.parse(atob(token.split('.')[1])) as { role: 'dosen' | 'mahasiswa'; username: string }
  } catch {
    localStorage.removeItem('ruangkampus_token')
    return null
  }
}

export function logout() {
  localStorage.removeItem('ruangkampus_token')
}

export function getApiBaseUrl() {
  return API_BASE_URL
}

async function request<T>(path: string, options: RequestInit = {}) {
  const headers = new Headers(options.headers)
  headers.set('Content-Type', 'application/json')
  const token = getToken()
  if (token) headers.set('Authorization', `Bearer ${token}`)

  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers })
  if (response.status === 401) {
    localStorage.removeItem('ruangkampus_token')
    throw new Error('Sesi login berakhir. Silakan login kembali.')
  }
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.message ?? `Request gagal (${response.status})`)
  }
  return response.json() as Promise<T>
}

export const api = {
  getClasses: () => request<ApiClass[]>('/kelas'),
  getCourses: () => request<ApiCourse[]>('/matkul'),
  getStudents: () => request<ApiStudent[]>('/mahasiswa'),
  getMyStudent: () => request<ApiStudent>('/mahasiswa/me'),
  getProfile: () => request<{ user: { role: string }; data: Record<string, unknown> }>('/me'),
  createClass: (nama_kelas: string) => request<{ id: number }>('/kelas', { method: 'POST', body: JSON.stringify({ nama_kelas }) }),
  createCourse: (payload: { nama_matakuliah: string; sks: number; id_kelas: number; id_dosen: number }) => request<{ id: number }>('/matkul', { method: 'POST', body: JSON.stringify(payload) }),
}
