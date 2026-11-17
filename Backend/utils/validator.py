"""
validator.py
Validasi input parameter untuk limit dan turunan.
"""
import sympy as sp

VALID_DIRECTIONS = {"+", "-", "both"}

def validate_derivative_order(n) -> int:
    try:
        n_int = int(n)
    except (TypeError, ValueError):
        raise ValueError("Orde turunan harus bilangan bulat.")
    if n_int < 1:
        raise ValueError("Orde turunan minimal 1.")
    if n_int > 10:
        raise ValueError("Orde turunan maksimal 10 (biar ga berat).")
    return n_int

def validate_limit_point(point) -> sp.Expr:
    if point is None:
        raise ValueError("Titik limit wajib diisi.")

    if isinstance(point, (int, float)):
        return sp.sympify(point)

    s = str(point).strip().lower()
    if s in ("oo", "inf", "infinity", "+oo", "+inf", "+infinity"):
        return sp.oo
    if s in ("-oo", "-inf", "-infinity"):
        return -sp.oo

    try:
        val = sp.sympify(s)
    except (sp.SympifyError, SyntaxError):
        raise ValueError(f"Titik limit tidak valid: {point!r}")

    if not val.is_number:
        raise ValueError(f"Titik limit harus berupa angka atau ±∞, bukan {point!r}")

    return val

def validate_direction(direction: str) -> str:
    if direction is None:
        return "both"
    d = str(direction).strip().lower()
    aliases = {
        "kanan": "+", "right": "+", "+": "+",
        "kiri": "-", "left": "-", "-": "-",
        "both": "both", "dua-arah": "both", "dua arah": "both",
    }
    if d not in aliases:
        raise ValueError(f"Arah limit tidak valid: {direction!r}. Gunakan '+', '-', atau 'both'.")
    return aliases[d]