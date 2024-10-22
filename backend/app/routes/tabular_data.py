from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.tabular_services import EmployeeSalesService


sales_data_bp = Blueprint('sales_data', __name__)  # Create a new blueprint for sales data
service = EmployeeSalesService()  # Instantiate the sales service

@sales_data_bp.route('/sales', methods=['POST'])
@jwt_required()
def add_sale():
    # Endpoint to add a new sale
    data = request.json  # Get JSON data from the request
    user_id = get_jwt_identity()  # Get the current user's identity from the JWT
    sale = service.add_sale(user_id, data['product_name'], data['quantity'], data['sale_amount'])  # Add the sale
    return jsonify({"id": sale.id, "product_name": sale.product_name}), 201  # Return the created sale

@sales_data_bp.route('/sales', methods=['GET'])
@jwt_required()
def get_sales():
    # Endpoint to retrieve all sales for the current user
    user_id = get_jwt_identity()  # Get the current user's identity from the JWT
    sales = service.get_sales_by_user(user_id)  # Get sales records for the user
    return jsonify([{"id": sale.id, "user_id": sale.user_id, "product_name": sale.product_name, "quantity": sale.quantity, "sale_amount": sale.sale_amount} for sale in sales]), 200  # Return sales data

@sales_data_bp.route('/sales/<int:sale_id>', methods=['PUT'])
@jwt_required()
def update_sale(sale_id):
    # Endpoint to update an existing sale
    updated_info = request.json  # Get updated data from the request
    user_id = get_jwt_identity()  # Get the current user's identity from the JWT
    sale = service.update_sale(sale_id, updated_info, user_id)  # Update the sale
    if sale:
        return jsonify({"id": sale.id, "product_name": sale.product_name}), 200  # Return updated sale
    return jsonify({"message": "Sale not found"}), 404  # Return error if not found

@sales_data_bp.route('/sales/<int:sale_id>', methods=['DELETE'])
@jwt_required()
def delete_sale(sale_id):
    # Endpoint to delete a sale
    user_id = get_jwt_identity()  # Get the current user's identity from the JWT
    if service.delete_sale(sale_id, user_id):
        return jsonify({"message": "Sale deleted successfully!"}), 200  # Return success message
    return jsonify({"message": "Sale not found"}), 404  # Return error if not found

@sales_data_bp.route('/sales/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    # Endpoint to get sales statistics for the current user
    user_id = get_jwt_identity()  # Get the current user's identity from the JWT
    stats = service.compute_statistics(user_id)  # Compute statistics for the user
    return jsonify(stats), 200  # Return statistics
