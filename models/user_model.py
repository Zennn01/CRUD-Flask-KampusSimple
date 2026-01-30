# models/user_model.py
from config.database import get_connection

class UserModel:

    @staticmethod
    def get_by_username(username):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_user, username, password, role
            FROM users
            WHERE username = %s
        """, (username,))

        user = cur.fetchone()
        cur.close()
        conn.close()
        return user


    @staticmethod
    def get_by_id(id_user):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_user, username, role
            FROM users
            WHERE id_user = %s
        """, (id_user,))

        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
