from flask_jwt_extended import JWTManager
from app import app, auth, image_processing, tabular_data, text_analysis , db
from flask_cors import CORS

jwt = JWTManager(app)
CORS(app)


#register blueprints here
app.register_blueprint(auth.auth_bp)
app.register_blueprint(tabular_data.sales_data_bp)  # Register the tabular data blueprint
app.register_blueprint(image_processing.image_processing_bp)
app.register_blueprint(text_analysis.text_analysis_bp)

@app.route('/')
def index():
    return 'hello worl'

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
