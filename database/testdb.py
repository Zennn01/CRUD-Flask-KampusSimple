from config.database import get_connection

conn = get_connection()
print("Koneksi berhasil:", conn)
conn.close()
