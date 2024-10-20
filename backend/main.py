from flask_jwt_extended import JWTManager
from app import create_app #, db
from flask_cors import CORS

app = create_app()
jwt = JWTManager(app)
CORS(app)

@app.route('/')
def index():
    return 'hello worl'

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)