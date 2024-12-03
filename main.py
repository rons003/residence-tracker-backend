from flask import Flask, json
from flask_cors import CORS
from models.database import db
from routes.resident_bp import resident_bp

# from routes.sap_bp import sap_bp
from flask_jwt_extended import JWTManager

UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_file("config.json", load=json.load)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

jwt = JWTManager(app)


db.init_app(app)

app.register_blueprint(resident_bp, url_prefix='/resident')
# with app.app_context():
#     db.drop_all()
#     db.create_all()
