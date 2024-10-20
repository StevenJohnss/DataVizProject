from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(600), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

class EmployeeSales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to link to User
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sale_amount = db.Column(db.Float, nullable=False)

    # Relationship to the User model for easy relationship access in my application code 
    user = db.relationship('User', backref='sales')

    def __repr__(self):
        return f'<Sale {self.product_name} by User {self.user_id}>'

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)

    user = db.relationship('User', backref='images')

    def __repr__(self):
        return f'<Image {self.filename} by User {self.user_id}>'

class EmployeeProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    summary = db.Column(db.Text, nullable=False)
    
    #One-to-One Relationship: Each EmployeeProfile is linked to one User
    user = db.relationship('User', backref='profile', uselist=False)

    def __repr__(self):
        return f'<EmployeeProfile {self.id} by User {self.user_id}>'
