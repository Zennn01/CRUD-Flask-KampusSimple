from flask import Blueprint, jsonify, g
from models.dosen_model import DosenModel
from middlewares.role_middleware import (
    login_required,
    dosen_only
)

dosen_bp = Blueprint("dosen", __name__)

# =====================================
# DOSEN → GET DATA DIRI SENDIRI
# =====================================
@dosen_bp.get("/dosen/me")
@login_required
@dosen_only
def get_my_dosen():
    id_user = g.user["id_user"]

    data = DosenModel.get_by_user(id_user)

    if not data:
        return jsonify({
            "message": "Data dosen tidak ditemukan"
        }), 404

    # data sudah dict → langsung return
    return jsonify(data), 200