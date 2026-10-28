/* oxlint-disable react/set-state-in-effect */
import * as React from 'react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { api, getToken, getTokenPayload, logout } from './api'
import Login from './Login'
import type { LoginRole } from './Login'

// API data replaces local prototype data after authenticated request.
function mapClass(item: { id_kelas: number; nama_kelas: string }): ClassItem { return { id: item.id_kelas, name: item.nama_kelas, students: 0 } }
function mapCourse(item: { id_matakuliah: number; nama_matakuliah: string; sks: number; nama_kelas?: string; nama_dosen?: string }): Course { return { id: item.id_matakuliah, name: item.nama_matakuliah, code: `MK-${item.id_matakuliah}`, sks: item.sks, className: item.nama_kelas ?? '-', lecturer: item.nama_dosen ?? '-' } }
function mapStudent(item: { id_mahasiswa: number; nama: string; nim: string; semester: number; id_kelas: number }, classNames: Map<number, string> = new Map()): Student { return { id: item.id_mahasiswa, name: item.nama, nim: item.nim, semester: item.semester, className: classNames.get(item.id_kelas) ?? `Kelas ${item.id_kelas}` } }

import {
  BookOpen,
  ChevronDown,
  GraduationCap,
  LayoutDashboard,
  LogOut,
  Menu,
  Plus,
  Search,
  Settings,
  Users,
  X,
} from 'lucide-react'
import './App.css'

type Role = 'dosen' | 'mahasiswa'
type Page = 'overview' | 'mahasiswa' | 'kelas' | 'matakuliah' | 'profil'

type ClassItem = { id: number; name: string; students: number }
type Course = { id: number; name: string; code: string; sks: number; className: string; lecturer: string }
type Student = { id: number; name: string; nim: string; semester: number; className: string }

const classes: ClassItem[] = [
  { id: 1, name: 'TI-1A', students: 28 },
  { id: 2, name: 'TI-1B', students: 26 },
  { id: 3, name: 'SI-3A', students: 31 },
]

const courses: Course[] = [
  { id: 1, name: 'Pemrograman Web', code: 'TI204', sks: 3, className: 'TI-1A', lecturer: 'Dr. Budi Santoso' },
  { id: 2, name: 'Basis Data', code: 'TI206', sks: 3, className: 'TI-1A', lecturer: 'Dr. Budi Santoso' },
  { id: 3, name: 'Analisis Sistem', code: 'SI301', sks: 2, className: 'SI-3A', lecturer: 'Dra. Siti Aminah' },
  { id: 4, name: 'Interaksi Manusia Komputer', code: 'TI208', sks: 3, className: 'TI-1B', lecturer: 'Dr. Budi Santoso' },
]

const students: Student[] = [
  { id: 1, name: 'Andi Saputra', nim: '20241001', semester: 2, className: 'TI-1A' },
  { id: 2, name: 'Nadia Putri', nim: '20241002', semester: 2, className: 'TI-1A' },
  { id: 3, name: 'Raka Wijaya', nim: '20231017', semester: 4, className: 'SI-3A' },
]

function App() {
  const tokenPayload = getTokenPayload()
  const [authenticated, setAuthenticated] = useState(Boolean(tokenPayload))
  const [role, setRole] = useState<Role>(tokenPayload?.role ?? 'dosen')

  const [page, setPage] = useState<Page>('overview')
  const [query, setQuery] = useState('')
  const [mobileOpen, setMobileOpen] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [classData, setClassData] = useState(classes)
  const [courseData, setCourseData] = useState(courses)
  const [studentData, setStudentData] = useState(students)
  const [apiError, setApiError] = useState('')
  const [profileData, setProfileData] = useState<Record<string, unknown> | null>(null)
  const [formName, setFormName] = useState('')
  const [formCode, setFormCode] = useState('')
  const [formSks, setFormSks] = useState('')
  const [formClassId, setFormClassId] = useState('')
  const [saving, setSaving] = useState(false)

  const loadApiData = useCallback(async () => {
    const [remoteClasses, remoteCourses] = await Promise.all([api.getClasses(), api.getCourses()])
    setClassData(remoteClasses.map(mapClass))
    setCourseData(remoteCourses.map(mapCourse))
    const classNames = new Map(remoteClasses.map((item) => [item.id_kelas, item.nama_kelas]))
    if (role === 'dosen') {
      const remoteStudents = await api.getStudents()
      setStudentData(remoteStudents.map((item) => mapStudent(item, classNames)))
    } else {
      const remoteStudent = await api.getMyStudent()
      setStudentData([mapStudent(remoteStudent, classNames)])
    }
  }, [role])

  // API bootstrap intentionally writes fetched data into component state.
  // oxlint-disable-next-line react/set-state-in-effect
  useEffect(() => {
    if (!getToken()) return
    Promise.all([loadApiData(), api.getProfile()])
      // oxlint-disable-next-line react/set-state-in-effect
      .then(([, profile]) => setProfileData(profile.data))
      .catch((error: Error) => setApiError(error.message))
  }, [role, loadApiData])

  const saveForm = async () => {
    if (!formName.trim()) { setApiError('Nama wajib diisi.'); return }
    setSaving(true)
    setApiError('')
    try {
      if (page === 'kelas') await api.createClass(formName.trim())
      else {
        const classId = Number(formClassId)
        const sks = Number(formSks)
        if (!classId || !sks) throw new Error('Kelas dan SKS wajib diisi.')
        await api.createCourse({ nama_matakuliah: formName.trim(), sks, id_kelas: classId, id_dosen: 1 })
      }
      await loadApiData()
      setShowForm(false)
      setFormName(''); setFormCode(''); setFormSks(''); setFormClassId('')
    } catch (error) { setApiError(error instanceof Error ? error.message : 'Gagal menyimpan data') }
    finally { setSaving(false) }
  }

  const handleLogout = () => { logout(); setAuthenticated(false) }

  const isDosen = role === 'dosen'
  const title = page === 'overview' ? 'Ringkasan akademik' : page === 'mahasiswa' ? 'Data mahasiswa' : page === 'kelas' ? 'Daftar kelas' : page === 'matakuliah' ? 'Mata kuliah' : 'Profil saya'
  const filteredStudents = useMemo(() => studentData.filter((student) => `${student.name} ${student.nim}`.toLowerCase().includes(query.toLowerCase())), [studentData, query])
  const filteredCourses = useMemo(() => courseData.filter((course) => `${course.name} ${course.code} ${course.className}`.toLowerCase().includes(query.toLowerCase())), [courseData, query])
  const filteredClasses = useMemo(() => classData.filter((item) => item.name.toLowerCase().includes(query.toLowerCase())), [classData, query])
  const visibleStudents = studentData.length
  const visibleClasses = classData.length
  const visibleCourses = courseData.length

  if (!authenticated) return <Login onSuccess={(nextRole: LoginRole) => { setRole(nextRole); setAuthenticated(true) }} />

  const navigate = (next: Page) => {
    if (!isDosen && next === 'mahasiswa') return
    setPage(next); setQuery(''); setMobileOpen(false)
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileOpen ? 'is-open' : ''}`}>
        <div className="brand"><span className="brand-mark"><GraduationCap size={21} /></span><span>RuangKampus</span></div>
        <div className="workspace-label">AKADEMIK / 2026</div>
        <nav className="nav-list">
          <NavItem icon={<LayoutDashboard size={18} />} label="Overview" active={page === 'overview'} onClick={() => navigate('overview')} />
          {isDosen && <NavItem icon={<Users size={18} />} label="Mahasiswa" active={page === 'mahasiswa'} onClick={() => navigate('mahasiswa')} />}
          <NavItem icon={<GraduationCap size={18} />} label="Kelas" active={page === 'kelas'} onClick={() => navigate('kelas')} />
          <NavItem icon={<BookOpen size={18} />} label="Mata kuliah" active={page === 'matakuliah'} onClick={() => navigate('matakuliah')} />
        </nav>
        <div className="sidebar-bottom">
          <NavItem icon={<Settings size={18} />} label="Profil saya" active={page === 'profil'} onClick={() => navigate('profil')} />
          <button className="logout-link" onClick={handleLogout}><LogOut size={18} /> Keluar</button>
          <div className="user-chip"><div className="avatar">{isDosen ? 'BS' : 'AS'}</div><div><strong>{isDosen ? 'Budi Santoso' : 'Andi Saputra'}</strong><small>{isDosen ? 'Dosen' : 'Mahasiswa'}</small></div><ChevronDown size={16} /></div>
        </div>
      </aside>
      {mobileOpen && <button className="scrim" aria-label="Tutup menu" onClick={() => setMobileOpen(false)} />}
      <main className="main-content">
        <header className="topbar"><button className="mobile-menu" onClick={() => setMobileOpen(true)} aria-label="Buka menu"><Menu /></button><div><p className="eyebrow">Selamat datang kembali, {isDosen ? 'Budi' : 'Andi'}.</p><h1>{title}</h1></div><div className="top-actions"><div className="role-badge">{isDosen ? 'Dosen' : 'Mahasiswa'}</div><div className="avatar avatar-top">{isDosen ? 'BS' : 'AS'}</div></div></header>
        <div className="content-wrap">
          {apiError && <div className="api-alert" role="alert">{apiError}</div>}
          {page === 'overview' && <Overview isDosen={isDosen} navigate={navigate} studentCount={visibleStudents} classCount={visibleClasses} courseCount={visibleCourses} recentStudents={studentData} />}
          {page === 'mahasiswa' && <DataPage title="Mahasiswa aktif" count={`${filteredStudents.length} dari ${visibleStudents} mahasiswa`} query={query} setQuery={setQuery} empty={query.length > 0 && filteredStudents.length === 0}><table><thead><tr><th>Mahasiswa</th><th>NIM</th><th>Semester</th><th>Kelas</th><th></th></tr></thead><tbody>{filteredStudents.map((student) => <tr key={student.id}><td><div className="person-cell"><div className="avatar small">{student.name.split(' ').map((part) => part[0]).join('').slice(0, 2)}</div><strong>{student.name}</strong></div></td><td>{student.nim}</td><td>Semester {student.semester}</td><td><span className="tag">{student.className}</span></td><td><button className="row-menu">•••</button></td></tr>)}</tbody></table></DataPage>}
          {page === 'kelas' && <DataPage title="Kelas" count={`${filteredClasses.length} dari ${visibleClasses} kelas terdaftar`} query={query} setQuery={setQuery} empty={query.length > 0 && filteredClasses.length === 0} action={isDosen ? <button className="primary-button" onClick={() => setShowForm(true)}><Plus size={17} /> Tambah kelas</button> : undefined}><div className="class-grid">{filteredClasses.map((item) => <div className="class-card" key={item.id}><div className="class-icon"><GraduationCap size={20} /></div><span className="muted-label">KELAS {String(item.id).padStart(2, '0')}</span><h3>{item.name}</h3><p>{item.students} mahasiswa terdaftar</p><div className="card-footer"><span>Semester 2</span>{isDosen && <button className="text-button" onClick={() => setShowForm(true)}>Kelola <span>→</span></button>}</div></div>)}</div></DataPage>}
          {page === 'matakuliah' && <DataPage title="Mata kuliah" count={`${filteredCourses.length} dari ${visibleCourses} mata kuliah`} query={query} setQuery={setQuery} empty={query.length > 0 && filteredCourses.length === 0} action={isDosen ? <button className="primary-button" onClick={() => setShowForm(true)}><Plus size={17} /> Tambah mata kuliah</button> : undefined}><table><thead><tr><th>Mata kuliah</th><th>Kode</th><th>SKS</th><th>Kelas</th><th>Dosen</th><th></th></tr></thead><tbody>{filteredCourses.map((course) => <tr key={course.id}><td><strong>{course.name}</strong></td><td className="muted-text">{course.code}</td><td>{course.sks}</td><td><span className="tag">{course.className}</span></td><td>{course.lecturer}</td><td><button className="row-menu">•••</button></td></tr>)}</tbody></table></DataPage>}
          {page === 'profil' && <Profile isDosen={isDosen} profileData={profileData} />}
        </div>
      </main>
      {showForm && <div className="modal-layer"><div className="modal"><button className="close-button" onClick={() => setShowForm(false)}><X size={19} /></button><span className="modal-kicker">DATA AKADEMIK</span><h2>Tambah {page === 'kelas' ? 'kelas' : 'mata kuliah'}</h2><p className="modal-copy">Data dikirim ke API Flask.</p><label>{page === 'kelas' ? 'Nama kelas' : 'Nama mata kuliah'}<input value={formName} onChange={(event) => setFormName(event.target.value)} placeholder={page === 'kelas' ? 'Contoh: TI-2A' : 'Contoh: Pemrograman Web'} /></label>{page === 'matakuliah' && <div className="form-row"><label>Kode<input value={formCode} onChange={(event) => setFormCode(event.target.value)} placeholder="TI204" /></label><label>SKS<input value={formSks} onChange={(event) => setFormSks(event.target.value)} type="number" placeholder="3" /></label><label>Kelas ID<input value={formClassId} onChange={(event) => setFormClassId(event.target.value)} type="number" placeholder="1" /></label></div>}<button className="primary-button full" onClick={saveForm} disabled={saving}>{saving ? 'Menyimpan...' : 'Simpan data'}</button></div></div>}
    </div>
  )
}

function NavItem({ icon, label, active, onClick }: { icon: React.ReactNode; label: string; active: boolean; onClick: () => void }) { return <button className={`nav-item ${active ? 'active' : ''}`} onClick={onClick}>{icon}<span>{label}</span></button> }
function DataPage({ title, count, query, setQuery, action, empty, children }: { title: string; count: string; query: string; setQuery: (value: string) => void; action?: React.ReactNode; empty?: boolean; children: React.ReactNode }) { return <section className="page-section"><div className="section-head"><div><span className="section-kicker">DIRECTORY</span><h2>{title}</h2><p>{count}</p></div>{action}</div><div className="toolbar"><div className="search-box"><Search size={17} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Cari data..." /></div><button className="filter-button">Terbaru <ChevronDown size={15} /></button></div>{empty ? <div className="empty-state">Tidak ada data untuk kata “{query}”.</div> : <div className="table-wrap">{children}</div>}</section> }
function Overview({ isDosen, navigate, studentCount, classCount, courseCount, recentStudents }: { isDosen: boolean; navigate: (page: Page) => void; studentCount: number; classCount: number; courseCount: number; recentStudents: Student[] }) { return <><section className="hero-panel"><div><span className="section-kicker light">RINGKASAN HARI INI</span><h2>Semua yang penting,<br /><em>di satu tempat.</em></h2><p>Kelola aktivitas akademik dengan lebih teratur dan tenang.</p></div><div className="hero-ornament"><span>SEMESTER<br />GENAP</span><strong>26</strong></div></section><section className="metrics"><Metric label="Mahasiswa aktif" value={String(studentCount)} note="Data dari API" /><Metric label="Kelas berjalan" value={String(classCount)} note="Data dari API" /><Metric label="Mata kuliah" value={String(courseCount)} note="Data dari API" /></section><section className="overview-grid"><div className="recent-panel"><div className="panel-heading"><div><span className="section-kicker">AKTIVITAS TERBARU</span><h2>{isDosen ? 'Mahasiswa terbaru' : 'Jadwal kuliah saya'}</h2></div><button className="text-button" onClick={() => navigate(isDosen ? 'mahasiswa' : 'matakuliah')}>Lihat semua <span>→</span></button></div>{recentStudents.slice(0, 3).map((student) => <div className="activity-row" key={student.id}><div className="avatar small">{student.name.slice(0, 2).toUpperCase()}</div><div><strong>{student.name}</strong><p>{student.className} · {student.nim}</p></div><span className="activity-time">Hari ini</span></div>)}</div><div className="quick-panel"><span className="section-kicker">AKSES CEPAT</span><h2>Mulai dari sini</h2><button onClick={() => navigate('kelas')}><GraduationCap size={18} /><span>Kelola kelas</span><b>→</b></button><button onClick={() => navigate('matakuliah')}><BookOpen size={18} /><span>Lihat mata kuliah</span><b>→</b></button></div></section></> }
function Metric({ label, value, note }: { label: string; value: string; note: string }) { return <div className="metric"><span>{label}</span><strong>{value}</strong><small>{note}</small></div> }
function Profile({ isDosen, profileData }: { isDosen: boolean; profileData: Record<string, unknown> | null }) { const name = String(profileData?.nama ?? (isDosen ? 'Budi Santoso' : 'Andi Saputra')); const identifier = String(profileData?.[isDosen ? 'nidn' : 'nim'] ?? (isDosen ? '0305017802' : '20241001')); const semester = String(profileData?.semester ?? '2'); return <section className="profile-layout"><div className="profile-intro"><div className="avatar profile-avatar">{name.split(' ').map((part) => part[0]).join('').slice(0, 2)}</div><span className="section-kicker">PROFIL PENGGUNA</span><h2>{name}</h2><p>{isDosen ? 'Dosen · Fakultas Teknologi Informasi' : 'Mahasiswa · Teknik Informatika'}</p></div><div className="profile-details"><div><span>Nama lengkap</span><strong>{name}</strong></div><div><span>{isDosen ? 'NIDN' : 'NIM'}</span><strong>{identifier}</strong></div><div><span>Peran</span><strong>{isDosen ? 'Dosen' : 'Mahasiswa'}</strong></div><div><span>{isDosen ? 'Program studi' : 'Semester'}</span><strong>{isDosen ? 'Teknik Informatika' : semester}</strong></div></div></section> }

export default App
