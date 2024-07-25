from flask import Blueprint, request, jsonify
from yolo.services.image_processing import process_image
from yolo.utils.file_utils import save_file, remove_file

analyze_bp = Blueprint('analyze', __name__)


@analyze_bp.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        file = request.files['image']
        file_path = save_file(file, 'uploads')
        results = process_image(file_path)
        remove_file(file_path)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})
