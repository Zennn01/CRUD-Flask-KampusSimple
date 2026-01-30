from .database import get_connection

def init_database():
    conn = get_connection()
    cur = conn.cursor()

    # ===== TABEL USERS (LOGIN JWT) =====
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id_user SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'mahasiswa', 'dosen')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # ===== TABEL KELAS =====
    cur.execute("""
        CREATE TABLE IF NOT EXISTS kelas (
            id_kelas SERIAL PRIMARY KEY,
            nama_kelas VARCHAR(100) NOT NULL
        );
    """)

    # ===== TABEL DOSEN =====
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dosen (
            id_dosen SERIAL PRIMARY KEY,
            id_user INT UNIQUE NOT NULL,
            nama VARCHAR(100) NOT NULL,
            nidn VARCHAR(30) UNIQUE,
            CONSTRAINT fk_dosen_user
                FOREIGN KEY (id_user)
                REFERENCES users(id_user)
                ON DELETE CASCADE
        );
    """)

    # ===== TABEL MAHASISWA =====
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mahasiswa (
            id_mahasiswa SERIAL PRIMARY KEY,
            id_user INT UNIQUE NOT NULL,
            nama VARCHAR(100) NOT NULL,
            nim VARCHAR(30) UNIQUE NOT NULL,
            semester INT,
            id_kelas INT,
            CONSTRAINT fk_mahasiswa_user
                FOREIGN KEY (id_user)
                REFERENCES users(id_user)
                ON DELETE CASCADE,
            CONSTRAINT fk_mahasiswa_kelas
                FOREIGN KEY (id_kelas)
                REFERENCES kelas(id_kelas)
                ON DELETE SET NULL
        );
    """)

    # ===== TABEL MATAKULIAH =====
    cur.execute("""
        CREATE TABLE IF NOT EXISTS matakuliah (
            id_matakuliah SERIAL PRIMARY KEY,
            nama_matakuliah VARCHAR(100) NOT NULL,
            sks INT NOT NULL,
            id_kelas INT,
            id_dosen INT,
            CONSTRAINT fk_matakuliah_kelas
                FOREIGN KEY (id_kelas)
                REFERENCES kelas(id_kelas)
                ON DELETE SET NULL,
            CONSTRAINT fk_matakuliah_dosen
                FOREIGN KEY (id_dosen)
                REFERENCES dosen(id_dosen)
                ON DELETE SET NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Database akademik + JWT login siap dipakai")
