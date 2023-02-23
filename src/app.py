# Importing all the necessary imports for the API to work properly
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin

# Importing necessary elmenets from models.py
from models import db, Users, Characters, Planets, Favorites    # Why is 'db' imported?

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle and serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def say_hello():
    user = Users.query.all()
    list_of_users = list(map(lambda user: user.serialize(), user))
    response_body = {
        "Message": "Hello, this is the list of our users up till today!",
        "List of Users": list_of_users
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    if user is None:
        response_body = {"Message": "There's no user with that user_id! Sorry!"}
        return jsonify(response_body), 404
    return jsonify(user.serialize()), 200

@app.route('/user/<int:user_id>/favorites',methods=['GET'])
def get_user_favorites(user_id):
    user_favorites = Favorites.query.filter_by(user_id=user_id).first() # all() ???
#    list_of_user_favorites = list(map(lambda user_favorite: user_favorite.serialize(), user_favorites))
    if user_favorites is None:
        response_body = {"Message": "No favorites to show!"}
        return jsonify(response_body), 404
    return jsonify(user_favorites.serialize()), 200

@app.route('/favorites/<int:favorites_id>', methods=['GET'])
def get_favorite(favorites_id):
   favorites = Favorites.query.filter_by(favorite_id=favorites_id).first()
   if favorites is None:
        response_body = {"Message": "No favorites to show!"}
        return jsonify(response_body), 404
   return jsonify(favorites.serialize()), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    list_of_characters = list(map(lambda character: character.serialize(), characters))
    response_body = {
        "Message": "These are all the characters created up till now.",
        "List of Characters": list_of_characters
    }
    return jsonify(response_body), 200

@app.route('/characters/<int:character_id>',methods=['GET']) # Check!
def get_character(character_id):
    character = Characters.query.filter_by(character_id=character_id).first()
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    list_of_planets = list(map(lambda planet: planet.serialize(), planets))
    response_body = {
        "Message": "These are all the planets up till now!",
        "list_of_planets": list_of_planets
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>',methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.filter_by(planet_id=planet_id).first()
    if planet is None:
        response_body = {"Message": "No planet to show!"}
        return jsonify(response_body), 404  
    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    body = json.loads(request.data)
    new_planet = Planets(planet_name=body["planet_name"], planet_url=body["planet_url"])
    # if planet url o planet name ya está cogido
    db.session.add(new_planet)
    db.session.commit()

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)