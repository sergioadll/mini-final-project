"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, House, Business

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all_users():
    all_users =  User.query.all()
    all_users_serialized = [user.serialize() for user in all_users]

    return jsonify(all_users_serialized), 200

@app.route('/house', methods=['GET'])
def get_all_products():
    all_houses =  House.query.all()
    all_houses_serialized = [house.serialize() for house in all_houses]

    return jsonify(all_houses_serialized), 200

@app.route('/business', methods=['GET'])
def get_all_businesses():
    all_businesses =  Business.query.all()
    all_businesses_serialized = [business.serialize() for business in all_businesses]

    return jsonify(all_businesses_serialized), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
