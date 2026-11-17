"""
parser.py
Normalisasi input fungsi dari user menjadi ekspresi sympy yang valid.
Contoh: "3x^2 + 2x" -> "3*x**2 + 2*x"
"""
import re
import sympy as sp

# Daftar nama fungsi yang dikenal sympy (biar ga dianggap variabel)
KNOWN_FUNCS = {
    "sin", "cos", "tan", "cot", "sec", "csc",
    "asin", "acos", "atan",
    "sinh", "cosh", "tanh",
    "exp", "log", "ln", "sqrt", "abs",
    "pi", "e",
}

def _insert_implicit_multiplication(expr: str) -> str:
    # 1) angka diikuti huruf/kurung: 3x -> 3*x, 2( -> 2*(
    expr = re.sub(r"(\d)([a-zA-Z(])", r"\1*\2", expr)

    # 2) huruf diikuti kurung buka, KECUALI kalau itu nama fungsi
    def _letter_paren(m):
        before = m.group(1)
        for fn in KNOWN_FUNCS:
            if fn.endswith(before):
                return m.group(0)
        return f"{before}*("

    expr = re.sub(r"([a-zA-Z])\(", _letter_paren, expr)

    # 3) kurung tutup diikuti huruf/angka/kurung buka: )x -> )*x
    expr = re.sub(r"\)([a-zA-Z0-9(])", r")*\1", expr)

    return expr

def normalize_input(raw: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("Input fungsi kosong.")

    expr = raw.strip()
    expr = expr.replace("^", "**")
    expr = re.sub(r"\bln\s*\(", "log(", expr) # ln -> log (sympy pakai log)
    expr = _insert_implicit_multiplication(expr)
    expr = re.sub(r"\s+", " ", expr).strip()
    
    return expr

def parse_expression(raw: str, var_name: str = "x") -> sp.Expr:
    normalized = normalize_input(raw)

    # Batasi simbol yang boleh muncul (keamanan: cegah eval liar)
    local_dict = {name: getattr(sp, name) for name in KNOWN_FUNCS if hasattr(sp, name)}
    local_dict[var_name] = sp.Symbol(var_name, real=True)

    try:
        expr = sp.sympify(normalized, locals=local_dict)
    except (sp.SympifyError, SyntaxError, TypeError) as e:
        raise ValueError(f"Ekspresi tidak valid: {raw!r} -> {e}")

    # Pastikan tidak ada simbol aneh yang tersisa
    allowed_symbols = {sp.Symbol(var_name, real=True)}
    free = expr.free_symbols - allowed_symbols
    if free:
        raise ValueError(f"Variabel tidak dikenal: {', '.join(str(s) for s in free)}. Gunakan variabel '{var_name}'.")

    return expr