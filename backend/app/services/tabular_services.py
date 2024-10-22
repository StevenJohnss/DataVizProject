from ..extension import db
from ..models.core import EmployeeSales
import pandas as pd

class EmployeeSalesService:
    def add_sale(self, user_id, product_name, quantity, sale_amount):
        # Create a new sale record
        new_sale = EmployeeSales(user_id=user_id, product_name=product_name, quantity=quantity, sale_amount=sale_amount)
        db.session.add(new_sale)  # Add the new sale to the session
        db.session.commit()  # Commit the session to save the sale
        return new_sale

    def get_all_sales(self):
        # Retrieve all sales records
        return EmployeeSales.query.all()

    def get_sales_by_user(self, user_id):
        # Retrieve all sales records for a specific user
        return EmployeeSales.query.filter_by(user_id=user_id).all()

    def update_sale(self, sale_id, updated_info, user_id):
        # Update an existing sale record
        sale = EmployeeSales.query.filter_by(id=sale_id, user_id=user_id).first()  # Ensure the sale belongs to the user
        if sale:
            sale.product_name = updated_info.get('product_name', sale.product_name)
            sale.quantity = updated_info.get('quantity', sale.quantity)
            sale.sale_amount = updated_info.get('sale_amount', sale.sale_amount)
            db.session.commit()  # Commit the changes
            return sale
        return None

    def delete_sale(self, sale_id, user_id):
        # Delete a sale record
        sale = EmployeeSales.query.filter_by(id=sale_id, user_id=user_id).first()  # Ensure the sale belongs to the user
        if sale:
            db.session.delete(sale)  # Remove the sale from the session
            db.session.commit()  # Commit the session to save changes
            return True
        return False

    def compute_statistics(self, user_id):
        # Compute statistics for sales of a specific user, grouped by product name
        sales = EmployeeSales.query.filter_by(user_id=user_id).all()
        if not sales:
            return {}

        # Create a DataFrame from the sales data
        df = pd.DataFrame([(sale.product_name, sale.sale_amount, sale.quantity) for sale in sales], 
                          columns=['product_name', 'sale_amount', 'quantity'])

        # Group by product_name
        grouped = df.groupby('product_name')

        # Calculate statistics for each product
        stats = {}
        for product_name, group in grouped:
            stats[product_name] = {
                "mean": float(group['sale_amount'].mean()),
                "median": float(group['sale_amount'].median()),
                "mode": group['sale_amount'].mode().tolist(),
                "quartiles": {
                    "Q1": float(group['sale_amount'].quantile(0.25)),
                    "Q2": float(group['sale_amount'].quantile(0.5)),
                    "Q3": float(group['sale_amount'].quantile(0.75)),
                },
                "outliers": group[(group['sale_amount'] < (group['sale_amount'].mean() - 3 * group['sale_amount'].std())) | 
                                  (group['sale_amount'] > (group['sale_amount'].mean() + 3 * group['sale_amount'].std()))]['sale_amount'].tolist(),
                "total_sales": float(group['sale_amount'].sum()),
                "total_quantity": int(group['quantity'].sum())
            }

        return stats
