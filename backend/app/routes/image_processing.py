from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.image_services import ImageService
from werkzeug.utils import secure_filename
import os
import base64

image_processing_bp = Blueprint('image_processing', __name__)
service = ImageService()

def encode_image_to_base64(filepath):
    with open(os.path.abspath(filepath), "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

@image_processing_bp.route('/images/upload', methods=['POST'])
@jwt_required()
def upload_images():
    user_id = get_jwt_identity()
    files = request.files.getlist('images')
    uploaded_images = []
    
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            upload_folder = 'uploads'
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            image = service.add_image(user_id, filename, filepath)
            uploaded_images.append({
                "id": image.id,
                "filename": image.filename,
                "filepath": image.filepath
            })

    return jsonify(uploaded_images), 201

@image_processing_bp.route('/images/histogram/<int:image_id>', methods=['GET'])
@jwt_required()
def get_histogram(image_id):
    user_id = get_jwt_identity()
    histogram = service.generate_histogram(image_id, user_id)
    return jsonify({"histogram": histogram}), 200

@image_processing_bp.route('/images/segment/<int:image_id>', methods=['GET'])
@jwt_required()
def segment_image(image_id):
    user_id = get_jwt_identity()
    mask = service.generate_segmentation_mask(image_id, user_id)
    return jsonify({"mask": encode_image_to_base64(f'uploads/{mask}')}), 200

@image_processing_bp.route('/images/manipulate/<int:image_id>', methods=['POST'])
@jwt_required()
def manipulate_image(image_id):
    user_id = get_jwt_identity()
    data = request.json
    manipulated_image = service.manipulate_image(image_id, data, user_id)
    return jsonify({"filename": encode_image_to_base64(f'uploads/{manipulated_image.filename}') }), 200

@image_processing_bp.route('/images', methods=['GET'])
@jwt_required()
def get_images():
    user_id = get_jwt_identity()
    images = service.get_user_images(user_id)
    
    image_data = [{
        "id": image.id,
        "filename": image.filename,
        "filepath": image.filepath,
        "user_id": image.user_id,
        "data": encode_image_to_base64(image.filepath)
    } for image in images]
    
    return jsonify(image_data), 200