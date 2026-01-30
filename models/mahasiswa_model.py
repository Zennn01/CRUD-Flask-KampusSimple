from config.database import get_connection

class MahasiswaModel:

    # =============================
    # DOSEN / ADMIN
    # =============================
    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id_mahasiswa, nama, nim, semester, id_kelas
            FROM mahasiswa
            ORDER BY id_mahasiswa
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def get_by_kelas(id_kelas):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id_mahasiswa, nama, nim, semester
            FROM mahasiswa
            WHERE id_kelas = %s
            ORDER BY nama
        """, (id_kelas,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    # =============================
    # MAHASISWA (JWT BASED)
    # =============================
    @staticmethod
    def get_by_user_id(id_user):
        """
        Dipakai untuk endpoint /mahasiswa/me
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id_mahasiswa, nama, nim, semester, id_kelas
            FROM mahasiswa
            WHERE id_user = %s
        """, (id_user,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    @staticmethod
    def get_matakuliah_by_user(id_user):
        """
        Mahasiswa hanya dapat matakuliah berdasarkan kelasnya
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                m.id_matakuliah,
                m.nama_matakuliah,
                m.sks
            FROM mahasiswa mh
            JOIN matakuliah m ON mh.id_kelas = m.id_kelas
            WHERE mh.id_user = %s
            ORDER BY m.nama_matakuliah
        """, (id_user,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    # =============================
    # ADMIN
    # =============================
    @staticmethod
    def create(data):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO mahasiswa (id_user, nama, nim, semester, id_kelas)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_mahasiswa
        """, (
            data["id_user"],
            data["nama"],
            data["nim"],
            data["semester"],
            data["id_kelas"]
        ))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id

    @staticmethod
    def update(id_mahasiswa, data):
        conn = get_connection()
        cur = conn.cursor()

        fields = []
        values = []

        for key, value in data.items():
            fields.append(f"{key} = %s")
            values.append(value)

        if not fields:
            return False

        query = f"""
            UPDATE mahasiswa
            SET {', '.join(fields)}
            WHERE id_mahasiswa = %s
        """

        values.append(id_mahasiswa)
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()
        return True

    @staticmethod
    def delete(id_mahasiswa):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM mahasiswa WHERE id_mahasiswa = %s", (id_mahasiswa,))
        conn.commit()
        cur.close()
        conn.close()
        return True
