from config.database import get_connection
from datetime import datetime 

class MahasiswaModel:
    
    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mahasiswa ORDER BY id_mahasiswa ASC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    
    @staticmethod
    def get_by_id(id_mahasiswa):
        conn = get_connection()
        cur = conn.cursor()

        query = "SELECT * FROM mahasiswa WHERE id_mahasiswa = %s"
        cur.execute(query, (id_mahasiswa,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        return row 
    
    @staticmethod
    def get_by_kelas(id_kelas):
        conn = get_connection()
        cur = conn.cursor()

        query = """
        SELECT id_mahasiswa, nama, tgl_lahir, alamat, semester
        FROM mahasiswa
        WHERE id_kelas = %s
        """

        cur.execute(query, (id_kelas,))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows
    
    @staticmethod
    def count_by_kelas(id_kelas):
        conn = get_connection()
        cur = conn.cursor()

        query = "SELECT COUNT(*) AS total FROM mahasiswa WHERE id_kelas = %s"
        cur.execute(query, (id_kelas,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        return row["total"] 



    @staticmethod
    def create(data):
        conn = get_connection()
        cur = conn.cursor()

        query = """
                INSERT INTO mahasiswa (nama, tgl_lahir, alamat, semester, id_kelas)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_mahasiswa
            """
        values = (
            data["nama"],
            data["tgl_lahir"],
            data["alamat"],
            data["semester"],
            data["id_kelas"]
        )

        cur.execute(query, values)

        result = cur.fetchone()
        new_id = result["id_mahasiswa"]
        
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
                UPDATE mahasiswa SET {','.join(fields)} WHERE id_mahasiswa = %s
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