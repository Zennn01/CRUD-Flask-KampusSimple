from flask import Blueprint, jsonify, request
from models.matakuliah_model import MatakuliahModel
from middlewares.role_middleware import (
    login_required,
    dosen_only
)

matakuliah_bp = Blueprint("matakuliah", __name__)

# ===============================
# DOSEN & MAHASISWA
# GET SEMUA MATAKULIAH
# ===============================
@matakuliah_bp.get("/matkul")
@login_required
def get_matakuliah():
    """
    - DOSEN  : boleh
    - MAHASISWA : boleh
    """
    return jsonify(MatakuliahModel.get_all())


# ===============================
# DOSEN SAJA
# CREATE MATAKULIAH
# ===============================
@matakuliah_bp.post("/matkul")
@login_required
@dosen_only
def create_matakuliah():
    payload = request.get_json()

    if not payload:
        return jsonify({"message": "JSON body kosong"}), 400

    new_id = MatakuliahModel.create(payload)
    return jsonify({
        "message": "Matakuliah berhasil ditambahkan",
        "id": new_id
    }), 201


# ===============================
# DOSEN SAJA
# UPDATE MATAKULIAH
# ===============================
@matakuliah_bp.put("/matkul/<int:id_matkul>")
@login_required
@dosen_only
def update_matakuliah(id_matkul):
    payload = request.get_json()

    if not payload:
        return jsonify({"message": "JSON body kosong"}), 400

    MatakuliahModel.update(id_matkul, payload)
    return jsonify({
        "message": "Matakuliah berhasil diupdate"
    })


# ===============================
# DOSEN SAJA
# DELETE MATAKULIAH
# ===============================
@matakuliah_bp.delete("/matkul/<int:id_matkul>")
@login_required
@dosen_only
def delete_matakuliah(id_matkul):
    MatakuliahModel.delete(id_matkul)
    return jsonify({
        "message": "Matakuliah berhasil dihapus"
    })
