import sympy as sp

def hitung_turunan(expr: sp.Expr, variabel: str, orde: int) -> str:
    x = sp.Symbol(variabel, real=True)
    
    try:
        hasil = sp.diff(expr, x, orde)
        return str(hasil)
    except Exception as e:
        raise ValueError(f"Gagal menghitung turunan: {e}")