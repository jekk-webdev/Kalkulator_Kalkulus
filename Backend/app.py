"""
app.py
Entry point utama untuk menjalankan server Flask.
"""
import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS

# Tambahkan folder root (parent dari 'Backend') ke sys.path
# Biar Flask bisa baca folder 'Frontend' dengan mudah
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "Frontend")

# Import routes dan database
from Backend.database import init_db
from Backend.routes.limit_route import limit_bp
from Backend.routes.derivative_route import derivative_bp

# Inisialisasi Flask
# static_folder diarahkan ke frontend biar bisa buka HTML/CSS/JS
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app) # Izinkan request dari domain berbeda (berguna buat localhost)

# Daftarkan Blueprint (Routes)
app.register_blueprint(limit_bp)
app.register_blueprint(derivative_bp)

# Route utama untuk nampilin index.html
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

if __name__ == "__main__":
    # Bikin database kalau belum ada
    init_db()
    print("Server berjalan di http://127.0.0.1:5000")
    # Jalankan server
    app.run(debug=True, port=5000)