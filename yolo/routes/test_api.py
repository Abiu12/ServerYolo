from flask import Blueprint, jsonify

test_api_bp = Blueprint('test_api', __name__)


@test_api_bp.route('/testapi', methods=['GET'])
def test_api():
    return jsonify("API is running")
