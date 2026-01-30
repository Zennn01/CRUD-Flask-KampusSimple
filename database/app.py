from flask import Flask, jsonify, request
from models.mahasiswa_model import MahasiswaModel
from models.kelas_model import KelasModel
from models.matakuliah_model import MatakuliahModel
from config.database import get_connection
import logging


app = Flask(__name__)

# ============================
#   ENDPOINT MAHASISWA
# ============================

@app.get("/mahasiswa")
def get_mahasiswa():
    data = MahasiswaModel.get_all()
    return jsonify(data)

@app.get("/mahasiswa/<int:id_mahasiswa>")
def get_mahasiswa_by_id(id_mahasiswa):
    data = MahasiswaModel.get_by_id(id_mahasiswa)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"message": "Kelas tidak ditemukan"}), 404
    
@app.get("/kelas/<int:id_kelas>/j")
def jumlah_mahasiswa(id_kelas):
    total = MahasiswaModel.count_by_kelas(id_kelas)
    return jsonify({
        "id_kelas": id_kelas,
        "jumlah_mahasiswa": total
    })

@app.get("/kelas/<int:id_kelas>/mhs")
def mahasiswa_kelas(id_kelas):
    data = MahasiswaModel.get_by_kelas(id_kelas)
    return jsonify(data)


@app.post("/mahasiswa")
def create_mahasiswa():
    payload = request.get_json()
    if not payload:
        return jsonify({"status": "error", "message": "Data JSON kosong"}), 400
    try:
        new_id = MahasiswaModel.create(payload)
        return jsonify({"status": "success", "id": new_id})
    except Exception as e:
        # Ini buat lihat error detail di console
        logging.error(f"Error saat bikin mahasiswa: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.put("/mahasiswa/<int:id>")
def update_mahasiswa(id):
    payload = request.get_json()

    if not payload:
        return jsonify({"status": "error", "message": "JSON body kosong"}), 400

    try:
        MahasiswaModel.update(id, payload)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.delete("/mahasiswa/<int:id>")
def delete_mahasiswa(id):
    try:
        MahasiswaModel.delete(id)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================
#   ENDPOINT KELAS
# ============================

@app.get("/kelas")
def get_kelas():
    data = KelasModel.get_all()
    return jsonify(data)


@app.post("/kelas")
def create_kelas():
    payload = request.get_json()

    if not payload:
        return jsonify({"status": "error", "message": "JSON body kosong"}), 400

    try:
        new_id = KelasModel.create(payload)
        return jsonify({"status": "success", "id": new_id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.put("/kelas/<int:id>")
def update_kelas(id):
    payload = request.get_json()

    if not payload:
        return jsonify({"status": "error", "message": "JSON body kosong"}), 400

    try:
        KelasModel.update(id, payload)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.delete("/kelas/<int:id>")
def delete_kelas(id):
    try:
        KelasModel.delete(id)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================
#   ENDPOINT MATAKULIAH
# ============================

@app.get("/matkul")
def get_matakuliah():
    data = MatakuliahModel.get_all()
    return jsonify(data)


@app.post("/matkul")
def create_matakuliah():
    payload = request.get_json()

    if not payload:
        return jsonify({"status": "error", "message": "JSON body kosong"}), 400

    try:
        new_id = MatakuliahModel.create(payload)
        return jsonify({"status": "success", "id": new_id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.put("/matkul/<int:id>")
def update_matakuliah(id):
    payload = request.get_json()

    if not payload:
        return jsonify({"status": "error", "message": "JSON body kosong"}), 400

    try:
        MatakuliahModel.update(id, payload)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.delete("/matkul/<int:id>")
def delete_matakuliah(id):
    try:
        MatakuliahModel.delete(id)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================
#   RUN SERVER
# ============================

if __name__ == "__main__":
    app.run(debug=True)