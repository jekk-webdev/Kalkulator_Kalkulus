from flask import Blueprint, request, jsonify
from ..utils.parser import parse_expression
from ..utils.validator import validate_limit_point, validate_direction
from ..services.limit_service import hitung_limit
from ..services.steps_limit import langkah_limit
from ..database import simpan_riwayat

limit_bp = Blueprint('limit_bp', __name__)

@limit_bp.route('/api/limit', methods=['POST'])
def proses_limit():
    data = request.get_json()
    if not data or 'fungsi' not in data:
        return jsonify({"error": "Input fungsi kosong"}), 400

    raw_fungsi = data.get('fungsi')
    raw_titik = data.get('titik')
    raw_arah = data.get('arah', 'both')

    try:
        # 1. Parse dan Validasi
        expr = parse_expression(raw_fungsi)
        titik = validate_limit_point(raw_titik)
        arah = validate_direction(raw_arah)

        # 2. Hitung Hasil Akhir & Langkah-langkah
        hasil = hitung_limit(expr, 'x', titik, arah)
        langkah = langkah_limit(expr, 'x', titik, arah)

        # 3. Simpan ke Database
        simpan_riwayat(
            tipe="limit",
            input_fungsi=raw_fungsi,
            parameter={"titik": str(raw_titik), "arah": arah},
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