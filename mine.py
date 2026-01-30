from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfigurasi koneksi ke PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost:5432/kampusdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model Database
class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(50), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(50), nullable=False)

# Route GET (ambil semua data)
@app.route('/get', methods=['GET'])
def get_data():
    all_data = Mahasiswa.query.all()
    output = []

    for mhs in all_data:
        output.append({
            "id": mhs.id,
            "nim": mhs.nim,
            "nama": mhs.nama,
            "kelas": mhs.kelas
        })

    return jsonify(output), 200

# Route POST (tambah data)
@app.route('/post', methods=['POST'])
def post_data():
    data = request.get_json()

    new_data = Mahasiswa(
        nim=data['nim'],
        nama=data['nama'],
        kelas=data['kelas']
    )

    db.session.add(new_data)
    db.session.commit()

    return jsonify({"message": "Data berhasil ditambahkan"}), 201

# Route PUT (update data)
@app.route('/update/<int:id>', methods=['PUT'])
def update_data(id):
    data = request.get_json()
    mhs = Mahasiswa.query.get_or_404(id)

    mhs.nim = data.get('nim', mhs.nim)
    mhs.nama = data.get('nama', mhs.nama)
    mhs.kelas = data.get('kelas', mhs.kelas)

    db.session.commit()

    return jsonify({"message": "Data berhasil diupdate"}), 200

# Route DELETE (hapus data)
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_data(id):
    mhs = Mahasiswa.query.get_or_404(id)

    db.session.delete(mhs)
    db.session.commit()

    return jsonify({"message": "Data berhasil dihapus"}), 200

# Running server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
