"""
steps_limit.py
Menampilkan langkah-langkah limit (scoped: substitusi & L'Hopital).
"""
import sympy as sp

def langkah_limit(expr: sp.Expr, variabel: str, titik: sp.Expr, arah: str) -> list:
    x = sp.Symbol(variabel, real=True)
    langkah = []
    
    langkah.append(f"Fungsi limit: lim(x -> {titik}) [{expr}]")
    
    # 1. Coba substitusi langsung
    try:
        substitusi = expr.subs(x, titik)
        if substitusi.is_number and not substitusi.is_infinite:
            langkah.append(f"Langkah 1: Substitusi langsung x = {titik}.")
            langkah.append(f"Hasil substitusi: {substitusi}")
            
            # Kalau hasilnya bukan 0/0, berarti selesai
            # Kalau hasilnya 0/0 (nan) atau tak hingga (zoo), jangan tampilkan angkanya
            if substitusi == sp.nan or substitusi == sp.zoo:
                langkah.pop() # Hapus baris "Hasil substitusi: nan" tadi
                langkah.pop() # Hapus baris "Langkah 1: Substitusi..."
            else:
                return langkah
    except:
        pass
        
    # 2. Kalau substitusi gagal (bentuk tak tentu 0/0 atau tak hingga/tak hingga)
    langkah.append("Langkah 2: Substitusi langsung menghasilkan bentuk tak tentu.")
    
    # Hitung pakai limit sympy (biasanya pakai L'Hopital di balik layar)
    arah_sympy = arah if arah in ['+', '-'] else '+-'
    hasil_limit = sp.limit(expr, x, titik, dir=arah_sympy)
    
    langkah.append(f"Langkah 3: Gunakan aturan L'Hôpital (turunkan pembilang dan penyebut).")
    langkah.append(f"Didapat hasil akhir limit = {hasil_limit}")
    
    return langkah