from flask import Blueprint, request, jsonify
from ..utils.parser import parse_expression
from ..utils.validator import validate_derivative_order
from ..services.derivative_service import hitung_turunan
from ..services.step_derivative import langkah_turunan
from ..database import simpan_riwayat

derivative_bp = Blueprint('derivative_bp', __name__)

@derivative_bp.route('/api/derivative', methods=['POST'])
def proses_turunan():
    data = request.get_json()
    if not data or 'fungsi' not in data:
        return jsonify({"error": "Input fungsi kosong"}), 400

    raw_fungsi = data.get('fungsi')
    raw_orde = data.get('orde', 1)

    try:
        # 1. Parse dan Validasi
        expr = parse_expression(raw_fungsi)
        orde = validate_derivative_order(raw_orde)

        # 2. Hitung Hasil Akhir & Langkah-langkah
        hasil = hitung_turunan(expr, 'x', orde)
        langkah = langkah_turunan(expr, 'x', orde)

        # 3. Simpan ke Database
        simpan_riwayat(
            tipe="turunan",
            input_fungsi=raw_fungsi,
            parameter={"orde": orde},
            hasil=hasil
        )

        # 4. Kembalikan response JSON ke Frontend
        return jsonify({
            "status": "sukses",
            "hasil": hasil,
            "langkah": langkah
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan sistem: {e}"}), 500