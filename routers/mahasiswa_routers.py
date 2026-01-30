from flask import Blueprint, jsonify, g
from models.mahasiswa_model import MahasiswaModel
from middlewares.role_middleware import (
    login_required,
    dosen_only,
    mahasiswa_only
)

mahasiswa_bp = Blueprint("mahasiswa", __name__)

# ===============================
# DOSEN → GET SEMUA MAHASISWA
# ===============================
@mahasiswa_bp.get("/mahasiswa")
@login_required
@dosen_only
def get_all_mahasiswa():
    return jsonify(MahasiswaModel.get_all())


# ======================================
# MAHASISWA → GET DATA DIRI SENDIRI
# ======================================
@mahasiswa_bp.get("/mahasiswa/me")
@login_required
@mahasiswa_only
def get_my_mahasiswa():
    user_id = g.user["id_user"]  # ✅ FIX DI SINI
    data = MahasiswaModel.get_by_user_id(user_id)

    if not data:
        return jsonify({
            "message": "Data mahasiswa tidak ditemukan"
        }), 404

    return jsonify(data)
