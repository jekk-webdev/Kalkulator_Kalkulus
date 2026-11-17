"""
steps_derivative.py
Menampilkan langkah-langkah turunan (scoped).
"""
import sympy as sp

def langkah_turunan(expr: sp.Expr, variabel: str, orde: int) -> list:
    x = sp.Symbol(variabel, real=True)
    langkah = []
    
    langkah.append(f"Fungsi awal: f(x) = {expr}")
    langkah.append(f"Kita akan mencari turunan orde ke-{orde} terhadap {variabel}.")
    
    current_expr = expr
    for i in range(1, orde + 1):
        # Hitung turunan ke-i
        current_expr = sp.diff(current_expr, x)
        
        # Kasih penjelasan sederhana (aturan pangkat)
        langkah.append(f"Langkah {i}: Turunkan setiap suku terhadap {variabel}.")
        langkah.append(f"Hasil turunan ke-{i}: {current_expr}")
        
    return langkah