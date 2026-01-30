from flask import Blueprint, jsonify, request
from models.kelas_model import KelasModel
from middlewares.role_middleware import (
    login_required,
    dosen_only
)

kelas_bp = Blueprint("kelas", __name__)

# ===============================
# DOSEN & MAHASISWA
# GET SEMUA KELAS
# ===============================
@kelas_bp.get("/kelas")
@login_required
def get_kelas():
    """
    - DOSEN  : boleh
    - MAHASISWA : boleh
    """
    return jsonify(KelasModel.get_all())


# ===============================
# DOSEN SAJA
# CREATE KELAS
# ===============================
@kelas_bp.post("/kelas")
@login_required
@dosen_only
def create_kelas():
    """
    - DOSEN  : boleh
    - MAHASISWA : tidak boleh
    """
    payload = request.get_json()

    if not payload:
        return jsonify({"message": "JSON body kosong"}), 400

    new_id = KelasModel.create(payload)
    return jsonify({
        "message": "Kelas berhasil ditambahkan",
        "id": new_id
    }), 201


# ===============================
# DOSEN SAJA
# UPDATE KELAS
# ===============================
@kelas_bp.put("/kelas/<int:id_kelas>")
@login_required
@dosen_only
def update_kelas(id_kelas):
    """
    - DOSEN  : boleh
    - MAHASISWA : tidak boleh
    """
    payload = request.get_json()

    if not payload:
        return jsonify({"message": "JSON body kosong"}), 400

    KelasModel.update(id_kelas, payload)
    return jsonify({
        "message": "Kelas berhasil diupdate"
    })


# ===============================
# DOSEN SAJA
# DELETE KELAS
# ===============================
@kelas_bp.delete("/kelas/<int:id_kelas>")
@login_required
@dosen_only
def delete_kelas(id_kelas):
    """
    - DOSEN  : boleh
    - MAHASISWA : tidak boleh
    """
    KelasModel.delete(id_kelas)
    return jsonify({
        "message": "Kelas berhasil dihapus"
    })
