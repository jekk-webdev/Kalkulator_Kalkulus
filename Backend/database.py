"""
database.py
Modul untuk mengelola database SQLite (riwayat perhitungan).
Hanya file ini yang boleh berisi perintah SQL.
"""
import sqlite3
import json
import os
from .config import DATABASE_PATH, DATA_DIR

def get_connection():
    """Membuat koneksi ke database SQLite."""
    # Pastikan folder 'data' ada sebelum bikin database
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    conn = sqlite3.connect(DATABASE_PATH)
    # Biar hasil query bisa diakses pakai nama kolom (bukan cuma index angka)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """Membuat tabel 'riwayat' kalau belum ada."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS riwayat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipe TEXT NOT NULL,
                input_fungsi TEXT NOT NULL,
                parameter TEXT,
                hasil TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def simpan_riwayat(tipe: str, input_fungsi: str, parameter: dict, hasil: str):
    """Menyimpan satu data perhitungan ke database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Parameter (seperti titik limit/orde) kita ubah jadi string JSON
        parameter_str = json.dumps(parameter) if parameter else None
        
        cursor.execute("""
            INSERT INTO riwayat (tipe, input_fungsi, parameter, hasil)
            VALUES (?, ?, ?, ?)
        """, (tipe, input_fungsi, parameter_str, hasil))
        conn.commit()

def ambil_riwayat():
    """Mengambil semua riwayat, diurutkan dari yang terbaru."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM riwayat ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        
        # Ubah format sqlite.Row jadi dict Python biasa biar gampang dikirim ke frontend
        hasil = []
        for row in rows:
            item = dict(row)
            # Balikin parameter dari string JSON jadi dict
            if item['parameter']:
                item['parameter'] = json.loads(item['parameter'])
            hasil.append(item)
        return hasil

def hapus_riwayat():
    """Menghapus semua riwayat."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM riwayat")
        conn.commit()