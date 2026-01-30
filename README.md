# CRUD Kampus simple

Mengambil data 
 http://127.0.0.1:5000/get
 
Menambah data menggunakan perintah jeson
{
  "nim": "20241001",
  "nama": "Andi Saputra",
  "kelas": "TI-1A"
}

http://127.0.0.1:5000/post

Update data menggunkan put berdasarkan ID lewat jeson 
{
  "nama": "Andi Setiawan",
  "kelas": "TI-1B"
}

http://127.0.0.1:5000/update/1

Menghapus Data Berdasarkan ID 
http://127.0.0.1:5000/delete/1
