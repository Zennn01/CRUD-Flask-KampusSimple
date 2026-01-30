from flask import Blueprint, request, jsonify
import jwt
from config.database import get_connection

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = "super-secret-key"

@auth_bp.post("/login")
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Data kosong"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username dan password wajib"}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id_user, username, role FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return jsonify({"message": "Login gagal"}), 401

    payload = {
        "id_user": user["id_user"],
        "username": user["username"],
        "role": user["role"]
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": "Login berhasil",
        "token": token,
    })
