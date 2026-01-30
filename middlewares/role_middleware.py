from flask import g, jsonify
from functools import wraps

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not hasattr(g, "user") or not g.user:
            return jsonify({
                "message": "Unauthorized, silakan login"
            }), 401
        return fn(*args, **kwargs)
    return wrapper

def dosen_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        if not hasattr(g, "user") or not g.user:
            return jsonify({
                "message": "Unauthorized, silakan login"
            }), 401

        if g.user.get("role") != "dosen":
            return jsonify({
                "message": "Akses khusus dosen"
            }), 403

        return fn(*args, **kwargs)

    return wrapper

def mahasiswa_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        if not hasattr(g, "user") or not g.user:
            return jsonify({
                "message": "Unauthorized, silakan login"
            }), 401

        if g.user.get("role") != "mahasiswa":
            return jsonify({
                "message": "Akses khusus mahasiswa"
            }), 403

        return fn(*args, **kwargs)

    return wrapper

def self_only(param_id="id"):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            if not hasattr(g, "user") or not g.user:
                return jsonify({"message": "Unauthorized"}), 401

            if g.user.get("id") != kwargs.get(param_id):
                return jsonify({
                    "message": "Hanya boleh mengakses data sendiri"
                }), 403

            return fn(*args, **kwargs)

        return wrapper
    return decorator
