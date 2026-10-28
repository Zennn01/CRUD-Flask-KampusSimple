# CRUD Flask Kampus

Sistem informasi akademik sederhana untuk mengelola data kampus. Project terdiri dari:

- Backend: Flask REST API + PostgreSQL + JWT.
- Frontend: React + TypeScript + Vite.
- Role pengguna: `dosen` dan `mahasiswa`.

## Fitur

### Dosen

- Login menggunakan JWT.
- Melihat data mahasiswa.
- Melihat, menambah, mengubah, dan menghapus kelas.
- Melihat, menambah, mengubah, dan menghapus mata kuliah.
- Melihat profil dosen.

### Mahasiswa

- Login menggunakan JWT.
- Melihat daftar kelas.
- Melihat mata kuliah.
- Melihat profil sendiri.

### Frontend

- Halaman login.
- Dashboard sesuai role.
- Search data mahasiswa, kelas, dan mata kuliah.
- Empty state ketika hasil search kosong.
- Responsive layout desktop dan mobile.
- Hover state dan animasi transisi.
- Penyimpanan token JWT di browser.

## Struktur Project

```text
CRUD-Flask-KampusSimple/
├── config/                  # Koneksi dan inisialisasi database
├── database/                # File database lama/pendukung
├── middlewares/             # JWT dan pembatasan role
├── models/                  # Query database
├── routers/                 # Endpoint REST API
├── setup/app.py             # Inisialisasi Flask dan blueprint
├── main.py                  # Entry point backend
├── frontend/                # React frontend
├── PRD_FRONTEND.md          # Dokumen kebutuhan frontend
└── README.md
```

## Prasyarat

Install:

- Python 3.10 atau lebih baru.
- PostgreSQL.
- Node.js 18 atau lebih baru.
- npm.

## Konfigurasi Database

Backend memakai PostgreSQL. Konfigurasi koneksi berada di:

```text
config/database.py
```

Sesuaikan nilai berikut dengan PostgreSQL lokal:

```python
host="localhost"
database="flaskdb"
user="postgres"
password="PASSWORD_POSTGRESQL"
```

Jangan commit password database. Gunakan environment variable sebelum project dipakai di production.

## Menjalankan Backend

Dari root project:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependency backend:

```bash
pip install Flask flask-cors psycopg2-binary PyJWT
```

Jalankan API:

```bash
python main.py
```

Backend tersedia di:

```text
http://127.0.0.1:5000
```

Backend menjalankan inisialisasi database saat aplikasi mulai. Pastikan PostgreSQL aktif dan database `flaskdb` sudah tersedia.

## Menjalankan Frontend

Buka terminal kedua:

```bash
cd frontend
npm install
npm run dev
```

Frontend biasanya tersedia di:

```text
http://127.0.0.1:5173
```

Jika port tersebut sedang digunakan, Vite dapat memilih port lain. Gunakan URL yang muncul di terminal.

### API URL Frontend

Default API URL:

```text
http://127.0.0.1:5000
```

Untuk mengganti API URL, buat file `frontend/.env.local`:

```env
VITE_API_BASE_URL=http://127.0.0.1:5000
```

File `.env.local` tidak boleh di-commit.

## Alur Login

1. Buka frontend.
2. Isi username dan password dari tabel `users` PostgreSQL.
3. Frontend mengirim `POST /login`.
4. Backend mengembalikan JWT.
5. Frontend menyimpan token di `localStorage` dengan key `ruangkampus_token`.
6. Role dibaca dari token.
7. Request API berikutnya memakai header:

```http
Authorization: Bearer <JWT_TOKEN>
```

Logout menghapus token dari browser.

## Endpoint API

### Login

```http
POST /login
Content-Type: application/json
```

Request:

```json
{
  "username": "username_kampus",
  "password": "password_kampus"
}
```

### Profil umum

```http
GET /me
Authorization: Bearer <JWT_TOKEN>
```

### Profil dosen

```http
GET /dosen/me
Authorization: Bearer <JWT_TOKEN>
```

### Profil mahasiswa

```http
GET /mahasiswa/me
Authorization: Bearer <JWT_TOKEN>
```

### Mahasiswa

Dosen saja:

```http
GET /mahasiswa
Authorization: Bearer <JWT_TOKEN>
```

### Kelas

```http
GET    /kelas
POST   /kelas
PUT    /kelas/<id_kelas>
DELETE /kelas/<id_kelas>
```

Payload tambah kelas:

```json
{
  "nama_kelas": "TI-1A"
}
```

Endpoint `POST`, `PUT`, dan `DELETE` hanya dapat dipakai dosen.

### Mata kuliah

```http
GET    /matkul
POST   /matkul
PUT    /matkul/<id_matkul>
DELETE /matkul/<id_matkul>
```

Payload tambah mata kuliah:

```json
{
  "nama_matakuliah": "Pemrograman Web",
  "sks": 3,
  "id_kelas": 1,
  "id_dosen": 1
}
```

Endpoint perubahan data hanya dapat dipakai dosen.

## Pengujian dan Build

Frontend lint:

```bash
cd frontend
npm run lint
```

Frontend production build:

```bash
npm run build
```

Preview hasil production build:

```bash
npm run preview
```

## Error Umum

### `Token diperlukan`

Frontend belum login atau token sudah dihapus. Login ulang.

### `Token tidak valid`

JWT tidak valid atau sudah kedaluwarsa. Hapus token browser dan login ulang.

### CORS error

Pastikan backend berjalan di port `5000` dan frontend berjalan di port yang diizinkan (`5173`, `5174`, atau `5175`).

### Database connection error

Periksa:

- PostgreSQL sedang aktif.
- Database `flaskdb` tersedia.
- Username dan password PostgreSQL benar.
- Konfigurasi `config/database.py` sesuai environment lokal.

## Catatan Pengembangan

- Backend tetap menjadi sumber data utama.
- Data frontend memakai fallback mock ketika token belum tersedia.
- Endpoint mahasiswa dan mata kuliah memiliki pembatasan role.
- Pagination backend belum tersedia.
- Registrasi, reset password, upload foto, dan export data belum tersedia.

## Status Git

Jangan commit file berikut:

```text
.env
.env.local
.venv/
__pycache__/
frontend/node_modules/
frontend/dist/
frontend/dogfood-output/
```
