import sympy as sp

def hitung_limit(expr: sp.Expr, variabel: str, titik: sp.Expr, arah: str) -> str:
    x = sp.Symbol(variabel, real=True)
    
        # SymPy butuh string '+', '-', atau '+-' untuk dua arah (both)
    arah_sympy = arah if arah in ['+', '-'] else '+-'
    
    try:
        hasil = sp.limit(expr, x, titik, dir=arah_sympy)
        if hasil == sp.oo:
            return "∞"
        elif hasil == -sp.oo:
            return "-∞"
        else:
            return str(hasil)
    except Exception as e:
        raise ValueError(f"Gagal menghitung limit: {e}")