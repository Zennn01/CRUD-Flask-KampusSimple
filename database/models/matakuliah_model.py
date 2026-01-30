from config.database import get_connection

class MatakuliahModel:
    
    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM matakuliah ORDER BY id_matakuliah ASC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def create(data):
        conn = get_connection()
        cur = conn.cursor()

        query = """
                INSERT INTO matakuliah (nama_matakuliah, sks, id_kelas, id_mahasiswa)
                VALUES (%s, %s, %s, %s )
                RETURNING id_matakuliah
            """
        values = (
            data["nama_matakuliah"],
            data["sks"],
            data["id_kelas"],
            data["id_mahasiswa"]
        )

        cur.execute(query, values)

        result = cur.fetchone()
        new_id = result["id_matakuliah"]
        
        conn.commit()
        cur.close()
        conn.close()

        return new_id

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
                UPDATE matakuliah SET {','.join(fields)} WHERE matakuliah = %s
            """
        
        values.append(id_matakuliah)
        cur.execute(query, values)
        conn.commit()

        cur.close()
        conn.close()
        
        return True

    @staticmethod
    def delete(id_matakuliah):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM matakuliah WHERE id_matakuliah = %s", (id_matakuliah,))
        conn.commit()
        cur.close()
        conn.close()
        return True