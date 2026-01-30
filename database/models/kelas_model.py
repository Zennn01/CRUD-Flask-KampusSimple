from config.database import get_connection

class KelasModel:
    
    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM kelas ORDER BY id_kelas ASC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    
    
    

    @staticmethod
    def create(data):
        conn = get_connection()
        cur = conn.cursor()

        query = """
                INSERT INTO kelas (nama_kelas)
                VALUES (%s )
                RETURNING id_kelas
            """
        values = (
            data["nama_kelas"],
        )

        cur.execute(query, values)

        result = cur.fetchone()
        new_id = result["id_kelas"]
        
        conn.commit()
        cur.close()
        conn.close()

        return new_id
    


    @staticmethod
    def update(id_kelas, data):
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
                UPDATE kelas SET {','.join(fields)} WHERE id_kelas = %s
            """
        
        values.append(id_kelas)
        cur.execute(query, values)
        conn.commit()

        cur.close()
        conn.close()
        
        return True

    @staticmethod
    def delete(id_kelas):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM kelas WHERE id_kelas = %s", (id_kelas,))
        conn.commit()
        cur.close()
        conn.close()
        return True