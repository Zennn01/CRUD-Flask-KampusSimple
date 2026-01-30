from models.mahasiswa_model import MahasiswaModel
from models.kelas_model import KelasModel
from models.matakuliah_model import MataKuliahModel

print("\n--- TEST MODEL MAHASISWA ---")
try:
    data = MahasiswaModel.get_all()
    print("Mahasiswa ->", data)
except Exception as e:
    print("Error Mahasiswa:", e)

print("\n--- TEST MODEL KELAS ---")
try:
    data = KelasModel.get_all()
    print("Kelas ->", data)
except Exception as e:
    print("Error Kelas:", e)

print("\n--- TEST MODEL MATAKULIAH ---")
try:
    data = MataKuliahModel.get_all()
    print("Mata Kuliah ->", data)
except Exception as e:
    print("Error Mata Kuliah:", e)
