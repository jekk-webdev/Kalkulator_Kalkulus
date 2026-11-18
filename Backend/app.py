"""
app.py
Entry point utama untuk menjalankan server Flask.
"""
import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv  # <--- Import dotenv

# 1. Muat file .env
load_dotenv()

# 2. Tentukan folder Frontend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "Frontend")

# 3. Import dari folder Backend
from Backend.database import init_db
from Backend.routes.limit_route import limit_bp
from Backend.routes.derivative_route import derivative_bp

# 4. Inisialisasi Flask
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

# 5. Daftarkan routes
app.register_blueprint(limit_bp)
app.register_blueprint(derivative_bp)

# 6. Halaman utama
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "tampilanWeb.html")

# 7. Nyalakan server
if __name__ == "__main__":
    init_db() # Bikin database kalau belum ada
    
    # Ambil port dari .env, kalau nggak ada pakai 5000
    port = int(os.getenv("PORT", 5000))
    
    print(f"Server berjalan di http://127.0.0.1:{port}")
    app.run(debug=True, port=port)