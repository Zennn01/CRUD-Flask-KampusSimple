from config.database import get_connection

class MatakuliahModel:

    # ===============================
    # DOSEN / ADMIN
    # ===============================
    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT m.id_matakuliah, m.nama_matakuliah, m.sks,
                   k.nama_kelas, d.nama AS nama_dosen
            FROM matakuliah m
            LEFT JOIN kelas k ON m.id_kelas = k.id_kelas
            LEFT JOIN dosen d ON m.id_dosen = d.id_dosen
            ORDER BY m.id_matakuliah ASC
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows


    @staticmethod
    def get_by_id(id_matakuliah):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT m.id_matakuliah, m.nama_matakuliah, m.sks,
                   k.nama_kelas, d.nama AS nama_dosen
            FROM matakuliah m
            LEFT JOIN kelas k ON m.id_kelas = k.id_kelas
            LEFT JOIN dosen d ON m.id_dosen = d.id_dosen
            WHERE m.id_matakuliah = %s
        """, (id_matakuliah,))

        row = cur.fetchone()
        cur.close()
        conn.close()
        return row


    # ===============================
    # MAHASISWA (JWT BASED)
    # ===============================
    @staticmethod
    def get_by_user(id_user):
        """
        Ambil matakuliah milik mahasiswa yang sedang login
        (BERDASARKAN TOKEN)
        """
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT m.id_matakuliah, m.nama_matakuliah, m.sks
            FROM matakuliah m
            JOIN kelas k ON m.id_kelas = k.id_kelas
            JOIN mahasiswa mh ON mh.id_kelas = k.id_kelas
            WHERE mh.id_user = %s
            ORDER BY m.nama_matakuliah
        """, (id_user,))

        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows


    # ===============================
    # CREATE
    # ===============================
    @staticmethod
    def create(data):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO matakuliah (nama_matakuliah, sks, id_kelas, id_dosen)
            VALUES (%s, %s, %s, %s)
            RETURNING id_matakuliah
        """, (
            data["nama_matakuliah"],
            data["sks"],
            data["id_kelas"],
            data["id_dosen"]
        ))

        new_id = cur.fetchone()["id_matakuliah"]
        conn.commit()
        cur.close()
        conn.close()
        return new_id


    # ===============================
    # UPDATE
    # ===============================
    @staticmethod
    def update(id_matakuliah, data):
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
            UPDATE matakuliah
            SET {', '.join(fields)}
            WHERE id_matakuliah = %s
        """

        values.append(id_matakuliah)
        cur.execute(query, values)
        conn.commit()

        cur.close()
        conn.close()
        return True


    # ===============================
    # DELETE
    # ===============================
    @staticmethod
    def delete(id_matakuliah):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM matakuliah WHERE id_matakuliah = %s",
            (id_matakuliah,)
        )

        conn.commit()
        cur.close()
        conn.close()
        return True
