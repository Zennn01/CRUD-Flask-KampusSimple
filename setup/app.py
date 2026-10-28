from flask import Flask
from flask_cors import CORS

# ===== ROUTERS =====
from routers.mahasiswa_routers import mahasiswa_bp
from routers.kelas_routers import kelas_bp
from routers.matakuliah_routers import matakuliah_bp
from routers.auth_router import auth_bp
from routers.dosen_router import dosen_bp
from routers.user_router import user_bp

# ===== CONFIG =====
from config.init_database import init_database
from middlewares.jwt_required import init_jwt

# =========================
# INIT FLASK APP
# =========================
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:5175", "http://localhost:5173", "http://localhost:5174", "http://localhost:5175"]}}, allow_headers=["Content-Type", "Authorization"])

# ===== SECRET KEY JWT =====
app.config["SECRET_KEY"] = "SECRET_KEY"

# ===== INIT DATABASE =====
init_database()

# ===== INIT JWT GLOBAL =====
init_jwt(app)

# ===== REGISTER BLUEPRINT =====
app.register_blueprint(auth_bp)
app.register_blueprint(mahasiswa_bp)
app.register_blueprint(kelas_bp)
app.register_blueprint(matakuliah_bp)
app.register_blueprint(dosen_bp)
app.register_blueprint(user_bp)
