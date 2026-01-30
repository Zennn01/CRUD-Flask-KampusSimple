# models/dosen_model.py
from config.database import get_connection

class DosenModel:

    @staticmethod
    def get_by_user(id_user):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_dosen, nama, nidn
            FROM dosen
            WHERE id_user = %s
        """, (id_user,))

        row = cur.fetchone()
        cur.close()
        conn.close()
        return row


