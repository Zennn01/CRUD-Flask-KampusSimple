from flask import request, jsonify, g
import jwt

SECRET_KEY = "super-secret-key"

EXCLUDE_PATHS = ["/login", "/auth/login"]

def init_jwt(app):

    @app.before_request
    def check_jwt():

        if request.path in EXCLUDE_PATHS:
            return

        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return jsonify({"message": "Token diperlukan"}), 401

        token = auth.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )
            g.user = payload
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token tidak valid"}), 401
