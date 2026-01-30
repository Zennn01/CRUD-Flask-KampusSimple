from config.database import get_connection

class KelasModel:

    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id_kelas, nama_kelas
            FROM kelas
            ORDER BY id_kelas ASC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(id_kelas):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id_kelas, nama_kelas
            FROM kelas
            WHERE id_kelas = %s
        """, (id_kelas,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    @staticmethod
    def create(data):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO kelas (nama_kelas)
            VALUES (%s)
            RETURNING id_kelas
        """, (data["nama_kelas"],))

        row = cur.fetchone()
        new_id = row["id_kelas"]

        conn.commit()
        cur.close()
        conn.close()

        return new_id

    @staticmethod
    def update(id_kelas, data):
        if not data:
            return False

        fields = []
        values = []

        for key, value in data.items():
            fields.append(f"{key} = %s")
            values.append(value)

        values.append(id_kelas)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"""
            UPDATE kelas
            SET {', '.join(fields)}
            WHERE id_kelas = %s
        """, values)

        updated = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()

        return updated > 0

    @staticmethod
    def delete(id_kelas):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM kelas
            WHERE id_kelas = %s
        """, (id_kelas,))

        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()

        return deleted > 0
