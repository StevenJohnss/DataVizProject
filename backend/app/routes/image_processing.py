from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.image_services import ImageService
from werkzeug.utils import secure_filename
import os

image_processing_bp = Blueprint('image_processing', __name__)
service = ImageService()

@image_processing_bp.route('/images/upload', methods=['POST'])
@jwt_required()
def upload_images():
    user_id = get_jwt_identity()
    files = request.files.getlist('images')  # Get list of uploaded files
    uploaded_images = []
    
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)  # Define your upload folder
            file.save(filepath)  # Save the file
            image = service.add_image(user_id, filename, filepath)  # Save image metadata
            uploaded_images.append({"id": image.id, "filename": image.filename})

    return jsonify(uploaded_images), 201

@image_processing_bp.route('/images/histogram/<int:image_id>', methods=['GET'])
@jwt_required()
def get_histogram(image_id):
    user_id = get_jwt_identity()
    histogram = service.generate_histogram(image_id, user_id)
    return jsonify(histogram), 200

@image_processing_bp.route('/images/segment/<int:image_id>', methods=['GET'])
@jwt_required()
def segment_image(image_id):
    user_id = get_jwt_identity()
    mask = service.generate_segmentation_mask(image_id, user_id)
    return jsonify({"mask": mask}), 200

@image_processing_bp.route('/images/manipulate/<int:image_id>', methods=['POST'])
@jwt_required()
def manipulate_image(image_id):
    user_id = get_jwt_identity()
    data = request.json
    manipulated_image = service.manipulate_image(image_id, data, user_id)
    return jsonify({"filename": manipulated_image.filename}), 200

