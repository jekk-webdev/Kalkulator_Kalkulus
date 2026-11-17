import os
import sys
import pytest
import sympy as sp

# Tambahin folder backend ke sys.path biar bisa import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from utils.parser import normalize_input, parse_expression

def test_power_caret():
    assert normalize_input("x^2") == "x**2"

def test_implicit_number_letter():
    assert normalize_input("3x") == "3*x"

def test_implicit_number_func():
    assert normalize_input("2sin(x)") == "2*sin(x)"

def test_letter_paren():
    assert normalize_input("x(x+1)") == "x*(x+1)"

def test_close_paren_open_paren():
    assert normalize_input("(x+1)(x-1)") == "(x+1)*(x-1)"

def test_ln_to_log():
    assert normalize_input("ln(x)") == "log(x)"

def test_parse_basic():
    expr = parse_expression("x^2 + 3x")
    x = sp.Symbol("x", real=True)
    assert sp.simplify(expr - (x**2 + 3*x)) == 0

def test_parse_fraction():
    expr = parse_expression("1/x")
    x = sp.Symbol("x", real=True)
    assert sp.simplify(expr - 1/x) == 0

def test_parse_sqrt():
    expr = parse_expression("sqrt(x)")
    x = sp.Symbol("x", real=True)
    assert sp.simplify(expr - sp.sqrt(x)) == 0

def test_parse_invalid_raises():
    with pytest.raises(ValueError):
        parse_expression("")

def test_parse_unknown_variable_raises():
    with pytest.raises(ValueError):
        parse_expression("x + y")