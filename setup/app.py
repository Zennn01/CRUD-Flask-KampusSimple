from flask import Flask

# ===== ROUTERS =====
from routers.mahasiswa_routers import mahasiswa_bp
from routers.kelas_routers import kelas_bp
from routers.matakuliah_routers import matakuliah_bp
from routers.auth_router import auth_bp
from routers.dosen_router import dosen_bp

# ===== CONFIG =====
from config.init_database import init_database
from middlewares.jwt_required import init_jwt

# =========================
# INIT FLASK APP
# =========================
app = Flask(__name__)

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
