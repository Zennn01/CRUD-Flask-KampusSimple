import { useState } from 'react'
import type { FormEvent } from 'react'
import { GraduationCap, LoaderCircle } from 'lucide-react'
import { getApiBaseUrl, login } from './api'
import './Login.css'

export type LoginRole = 'dosen' | 'mahasiswa'
type Props = { onSuccess: (role: LoginRole) => void }

export default function Login({ onSuccess }: Props) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setError('')
    if (!username.trim() || !password) {
      setError('Username dan password wajib diisi.')
      return
    }
    setLoading(true)
    try {
      const response = await login(username.trim(), password)
      const payload = JSON.parse(atob(response.token.split('.')[1])) as { role?: 'dosen' | 'mahasiswa' }
      if (payload.role !== 'dosen' && payload.role !== 'mahasiswa') throw new Error('Role pengguna tidak valid.')
      onSuccess(payload.role)
    } catch (loginError) {
      setError(loginError instanceof Error ? loginError.message : 'Login gagal')
    } finally {
      setLoading(false)
    }
  }

  return <main className="login-page">
    <section className="login-visual"><div className="login-brand"><span className="brand-mark"><GraduationCap size={22} /></span> RuangKampus</div><div><span className="login-kicker">SISTEM INFORMASI AKADEMIK</span><h1>Ruang belajar,<br /><em>lebih tertata.</em></h1><p>Kelola aktivitas akademik dalam satu ruang yang tenang dan terarah.</p></div><small>API: {getApiBaseUrl()}</small></section>
    <section className="login-panel"><div className="login-form-wrap"><span className="login-kicker">SELAMAT DATANG</span><h2>Masuk ke akunmu</h2><p className="login-copy">Gunakan akun kampus untuk melanjutkan.</p><form onSubmit={handleSubmit}><label>Username<input value={username} onChange={(event) => setUsername(event.target.value)} placeholder="Contoh: dosen01" autoComplete="username" /></label><label>Password<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Masukkan password" autoComplete="current-password" /></label>{error && <p className="login-error" role="alert">{error}</p>}<button className="login-button" disabled={loading}>{loading && <LoaderCircle size={17} className="spin" />}{loading ? 'Memeriksa akun...' : 'Masuk'}</button></form></div></section>
  </main>
}
