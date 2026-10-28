# PRD Frontend Sistem Informasi Kampus

## 1. Ringkasan Produk

Frontend web untuk mengakses backend Flask API Sistem Informasi Kampus. Sistem menampilkan data akademik dan membatasi fitur berdasarkan role pengguna:

- Dosen: mengelola kelas dan mata kuliah, melihat seluruh data mahasiswa.
- Mahasiswa: melihat data diri, daftar kelas, dan mata kuliah sesuai kelas.

Frontend menggunakan HTML, CSS, dan JavaScript. Backend tetap menjadi sumber data utama melalui REST API.

## 2. Tujuan

- Menyediakan login berbasis username dan password.
- Menampilkan dashboard sesuai role pengguna.
- Memudahkan dosen mengelola data akademik.
- Memudahkan mahasiswa melihat informasi akademiknya.
- Menampilkan pesan loading, sukses, gagal, dan akses ditolak dengan jelas.

## 3. Target Pengguna

### Dosen

Kebutuhan:

- Login ke sistem.
- Melihat seluruh mahasiswa.
- Melihat seluruh kelas.
- Menambah, mengubah, dan menghapus kelas.
- Melihat seluruh mata kuliah.
- Menambah, mengubah, dan menghapus mata kuliah.
- Melihat profil dosen.

### Mahasiswa

Kebutuhan:

- Login ke sistem.
- Melihat profil atau data diri sendiri.
- Melihat seluruh daftar kelas.
- Melihat mata kuliah sesuai kelasnya.
- Melihat profil mahasiswa.

## 4. Ruang Lingkup Versi Pertama

### Termasuk

- Halaman login.
- Penyimpanan JWT token di browser.
- Redirect berdasarkan role.
- Dashboard dosen.
- Dashboard mahasiswa.
- Sidebar atau navbar.
- Halaman data mahasiswa.
- Halaman data kelas.
- Halaman data mata kuliah.
- Halaman profil pengguna.
- Modal atau form tambah/edit data.
- Dialog konfirmasi hapus.
- Logout.
- Penanganan token tidak valid atau kedaluwarsa.
- Tampilan responsive untuk desktop dan mobile.

### Tidak termasuk versi pertama

- Registrasi pengguna.
- Reset password.
- Upload foto profil.
- Export Excel atau PDF.
- Notifikasi email.
- Pendaftaran mata kuliah oleh mahasiswa.
- Manajemen user dari frontend.
- Pagination backend.

## 5. Struktur Halaman

### 5.1 Login `/login`

Komponen:

- Logo atau nama aplikasi.
- Input username.
- Input password.
- Tombol Login.
- Pesan error login.
- Indikator loading.

Perilaku:

- Validasi input wajib diisi.
- Kirim `POST /login`.
- Simpan token dari response.
- Baca role dari token atau ambil data profil.
- Redirect dosen ke `/dosen/dashboard`.
- Redirect mahasiswa ke `/mahasiswa/dashboard`.
- Jika gagal, tampilkan `Login gagal`.

### 5.2 Dashboard Dosen `/dosen/dashboard`

Komponen:

- Ringkasan jumlah mahasiswa.
- Ringkasan jumlah kelas.
- Ringkasan jumlah mata kuliah.
- Nama dosen yang sedang login.
- Shortcut ke halaman mahasiswa, kelas, dan mata kuliah.
- Sidebar navigasi.
- Tombol logout.

Catatan: endpoint jumlah data khusus belum tersedia. Versi pertama dapat menghitung jumlah dari response endpoint daftar.

### 5.3 Dashboard Mahasiswa `/mahasiswa/dashboard`

Komponen:

- Nama mahasiswa.
- NIM.
- Semester.
- Kelas.
- Jumlah mata kuliah.
- Daftar mata kuliah ringkas.
- Tombol menuju profil.
- Tombol logout.

### 5.4 Data Mahasiswa `/dosen/mahasiswa`

Akses: dosen saja.

Komponen:

- Tabel mahasiswa.
- Kolom: No, Nama, NIM, Semester, ID Kelas.
- Search berdasarkan nama atau NIM di sisi frontend.
- State kosong jika data belum ada.
- State error jika request gagal.

Endpoint:

```text
GET /mahasiswa
Authorization: Bearer <token>
```

Catatan: backend saat ini hanya menyediakan GET daftar mahasiswa. Form tambah, edit, dan hapus belum tersedia di router aktif.

### 5.5 Data Kelas `/kelas`

Akses:

- Dosen: lihat, tambah, edit, hapus.
- Mahasiswa: lihat saja.

Komponen:

- Tabel atau kartu kelas.
- Kolom: ID Kelas, Nama Kelas.
- Tombol Tambah Kelas untuk dosen.
- Tombol Edit untuk dosen.
- Tombol Hapus untuk dosen.
- Form nama kelas.
- Dialog konfirmasi hapus.

Endpoint:

```text
GET /kelas
POST /kelas
PUT /kelas/<id_kelas>
DELETE /kelas/<id_kelas>
```

Payload tambah/edit:

```json
{
  "nama_kelas": "TI-1A"
}
```

### 5.6 Data Mata Kuliah `/matkul`

Akses:

- Dosen: lihat, tambah, edit, hapus.
- Mahasiswa: lihat mata kuliah sesuai kelas.

Komponen dosen:

- Tabel mata kuliah.
- Kolom: ID, Nama Mata Kuliah, SKS, Kelas, Dosen.
- Tombol Tambah.
- Tombol Edit.
- Tombol Hapus.
- Form nama mata kuliah, SKS, kelas, dan dosen.

Komponen mahasiswa:

- Kartu atau tabel mata kuliah milik kelasnya.
- Kolom: Nama Mata Kuliah dan SKS.
- Tanpa tombol perubahan data.

Endpoint:

```text
GET /matkul
POST /matkul
PUT /matkul/<id_matkul>
DELETE /matkul/<id_matkul>
```

Payload tambah/edit:

```json
{
  "nama_matakuliah": "Pemrograman Web",
  "sks": 3,
  "id_kelas": 1,
  "id_dosen": 1
}
```

Catatan: endpoint aktif `GET /matkul` mengembalikan data umum. Endpoint khusus mata kuliah mahasiswa belum didaftarkan pada router aktif, meskipun model memiliki method terkait.

### 5.7 Profil `/profile`

Dosen:

```text
GET /dosen/me
```

Mahasiswa:

```text
GET /mahasiswa/me
```

Komponen:

- Nama.
- NIDN untuk dosen.
- NIM untuk mahasiswa.
- Semester untuk mahasiswa.
- Kelas untuk mahasiswa jika tersedia.
- Tampilan read-only.

## 6. Matriks Hak Akses

| Fitur | Dosen | Mahasiswa |
|---|---:|---:|
| Login | Ya | Ya |
| Lihat profil sendiri | Ya | Ya |
| Lihat semua mahasiswa | Ya | Tidak |
| Lihat semua kelas | Ya | Ya |
| Tambah kelas | Ya | Tidak |
| Edit kelas | Ya | Tidak |
| Hapus kelas | Ya | Tidak |
| Lihat mata kuliah | Ya | Ya |
| Tambah mata kuliah | Ya | Tidak |
| Edit mata kuliah | Ya | Tidak |
| Hapus mata kuliah | Ya | Tidak |
| Logout | Ya | Ya |

## 7. Kontrak API

### Login

Request:

```http
POST /login
Content-Type: application/json
```

```json
{
  "username": "dosen01",
  "password": "password"
}
```

Response sukses:

```json
{
  "message": "Login berhasil",
  "token": "<JWT_TOKEN>"
}
```

Semua endpoint protected memakai header:

```http
Authorization: Bearer <JWT_TOKEN>
```

### Error umum

Frontend harus menangani:

- `400`: input atau JSON tidak valid.
- `401`: login gagal atau token tidak valid.
- `403`: role tidak memiliki akses.
- `404`: data tidak ditemukan.
- `500`: kesalahan server.
- Network error: backend tidak berjalan atau URL API salah.

## 8. Alur Utama

### Alur login

1. Pengguna membuka `/login`.
2. Pengguna mengisi username dan password.
3. Frontend memanggil `POST /login`.
4. Jika sukses, token disimpan.
5. Frontend membaca role dari JWT payload.
6. Frontend mengarahkan pengguna ke dashboard role.
7. Jika gagal, pesan error tampil.

### Alur request protected

1. JavaScript mengambil token dari storage.
2. JavaScript mengirim header `Authorization`.
3. Jika response `401`, token dihapus.
4. Pengguna diarahkan kembali ke login.
5. Jika response `403`, tampilkan pesan akses ditolak.

### Alur CRUD kelas atau mata kuliah

1. Dosen klik Tambah atau Edit.
2. Frontend membuka form modal.
3. Frontend memvalidasi input.
4. Frontend mengirim POST atau PUT.
5. Jika sukses, modal ditutup.
6. Data tabel dimuat ulang.
7. Jika gagal, pesan error tampil.

## 9. Kebutuhan UI/UX

- Desain bersih dengan nuansa sistem akademik.
- Sidebar desktop dan menu mobile.
- Warna utama biru tua atau indigo.
- Warna sukses hijau.
- Warna error merah.
- Tombol aksi memiliki label atau tooltip jelas.
- Tombol hapus memakai konfirmasi.
- Loading state tampil saat request berlangsung.
- Empty state tampil jika tabel kosong.
- Error state memiliki tombol Coba Lagi.
- Form memiliki label, bukan placeholder saja.
- Tabel tidak pecah pada layar kecil.
- Token tidak pernah ditampilkan di UI.

## 10. Struktur Frontend yang Disarankan

```text
templates/
├── login.html
├── layouts/
│   └── base.html
├── dosen/
│   ├── dashboard.html
│   ├── mahasiswa.html
│   ├── kelas.html
│   ├── matakuliah.html
│   └── profile.html
└── mahasiswa/
    ├── dashboard.html
    ├── kelas.html
    ├── matakuliah.html
    └── profile.html

static/
├── css/
│   ├── style.css
│   ├── auth.css
│   └── dashboard.css
└── js/
    ├── api.js
    ├── auth.js
    ├── guard.js
    ├── dosen.js
    └── mahasiswa.js
```

## 11. Acceptance Criteria

- Pengguna dapat login dengan akun valid.
- Pengguna melihat dashboard sesuai role.
- Mahasiswa tidak melihat tombol tambah, edit, atau hapus.
- Dosen dapat melihat daftar mahasiswa.
- Dosen dapat CRUD kelas melalui UI.
- Dosen dapat CRUD mata kuliah melalui UI.
- Mahasiswa dapat melihat data dirinya.
- Mahasiswa dapat melihat kelas dan mata kuliah yang diizinkan.
- Token dikirim pada semua endpoint protected.
- Token invalid mengarahkan pengguna ke login.
- Logout menghapus token dan menutup akses halaman protected.
- Error API tampil sebagai pesan yang mudah dipahami.
- Tampilan dapat dipakai pada desktop dan mobile.

## 12. Catatan Implementasi Backend

Backend aktif belum menyediakan route CRUD mahasiswa dan belum mendaftarkan endpoint khusus mata kuliah mahasiswa. PRD frontend tidak menganggap endpoint tersebut sudah tersedia.

Sebelum membuat UI penuh, pastikan endpoint berikut benar-benar tersedia jika fitur tersebut diperlukan:

```text
POST /mahasiswa
PUT /mahasiswa/<id_mahasiswa>
DELETE /mahasiswa/<id_mahasiswa>
GET /mahasiswa/me/matkul
```

Jika endpoint belum dibuat, frontend hanya menampilkan fitur yang didukung endpoint aktif.
