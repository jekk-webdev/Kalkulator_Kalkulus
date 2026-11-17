"""
config.py
File konfigurasi pusat untuk aplikasi kalkulator kalkulus.
Semua pengaturan (path database, mode debug) ditaruh di sini.
"""
import os

# 1. Tentukan direktori utama proyek (root folder)
# __file__ itu lokasi config.py, kita naik 2 level ke atas biar dapet folder utama
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Lokasi folder database dan nama file SQLite-nya
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE_PATH = os.path.join(DATA_DIR, "riwayat.db")

# 3. Pengaturan Flask
DEBUG_MODE = True
PORT = 5000