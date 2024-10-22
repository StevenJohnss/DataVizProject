from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.text_services import TextService

text_analysis_bp = Blueprint('text_analysis', __name__)
service = TextService()

@text_analysis_bp.route('/text/analyze', methods=['POST'])
@jwt_required()
def analyze_text():
    data = request.json
    user_id = get_jwt_identity()
    content = data.get('summary')

    if not content:
        return jsonify({"error": "Content is required"}), 400

    summary, keywords, sentiment = service.analyze_text(content, user_id)
    return jsonify({
        "summary": summary,
        "keywords": keywords,
        "sentiment": sentiment
    }), 200

@text_analysis_bp.route('/text/visualize', methods=['POST'])
@jwt_required()
def visualize_text():
    data = request.json
    user_id = get_jwt_identity()
    content = data.get('summary')

    if not content:
        return jsonify({"error": "Content is required"}), 400

    visualization = service.generate_text_visualization(content)
    return jsonify(visualization), 200

@text_analysis_bp.route('/text/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    data = request.json
    user_id = get_jwt_identity()
    new_summary = data.get('summary')

    if not new_summary:
        return jsonify({"error": "New summary is required"}), 400

    updated_profile = service.update_profile_summary(user_id, new_summary)
    if updated_profile:
        return jsonify({"msg": "Profile updated successfully", "summary": updated_profile.summary}), 200
    return jsonify({"error": "Profile not found"}), 404

@text_analysis_bp.route('/text/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user, profile = service.get_profile_by_user_id(user_id)

    resp= {"name": user.email.split("@")[0] , "email": user.email}
    if profile:
        profile = profile[0]
        resp["summary"] = profile.summary
        resp["id"] = profile.id
    
    return jsonify(resp), 200
