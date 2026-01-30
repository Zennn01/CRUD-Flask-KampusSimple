from flask import Blueprint, jsonify, g
from middlewares.jwt_required import jwt_required
from config.database import get_connection

user_bp = Blueprint("user", __name__)

@user_bp.get("/me")
@jwt_required
def get_me():
    user = g.user
    role = user["role"]
    id_user = user["id_user"]

    conn = get_connection()
    cur = conn.cursor()

    # ===== JIKA MAHASISWA =====
    if role == "mahasiswa":
        cur.execute("""
            SELECT id_mahasiswa, nama, nim, semester, id_kelas
            FROM mahasiswa
            WHERE id_user = %s
        """, (id_user,))
        data = cur.fetchone()

    # ===== JIKA DOSEN =====
    elif role == "dosen":
        cur.execute("""
            SELECT id_dosen, nama, nidn
            FROM dosen
            WHERE id_user = %s
        """, (id_user,))
        data = cur.fetchone()

    else:
        data = {"message": "Role tidak dikenali"}

    cur.close()
    conn.close()

    return jsonify({
        "user": user,
        "data": data
    })
