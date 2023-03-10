# 1.- «Cranear» lo de los favoritos
# 2.- Aplicar capas de autentificación

# Importing all the necessary imports for the API to work properly
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate # For migrations
from flask_swagger import swagger
from flask_cors import CORS # To avoid CORS domain errors
from utils import APIException, generate_sitemap # To manage exceptions and to create the sitemap object
from admin import setup_admin # Imports the set up of the admin's back-office

# Importing necessary elements from models.py
from models import db, Users, Characters, Planets, Favorites, Vehicles ############ Why is 'db' imported? ############

# JWT Imports
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__) # It adds a new Flask API
app.url_map.strict_slashes = False # With or without the final slash, the URL should work as expected

# Database Configuration —"DATABASE_URL" refers to the .env file
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)  # For the migration
db.init_app(app)            # Initializing the app
CORS(app)                   # Applying the CORS
setup_admin(app)            # Setting up the admin

# Handle and serialize errors like a JSON object
# (aka "Make the exceptions look prettier")
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "my-super-secret-key"  # Change this!
jwt = JWTManager(app)

# Generate sitemap with all your endpoints
# (aka "URL that lists all the endpoints")
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Defining the routes for the API

# Signup route (aka "Create User")
@app.route("/signup", methods=["POST"])
def signup():
    body = json.loads(request.data)
    this_user = Users.query.filter_by(user_email=body["email"]).first()
    if this_user is not None:
        return jsonify({"Message": "An user already exists with this email!"}), 400
    new_user = Users(user_email=body["email"], user_password=body["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"Message": "User created successfully!"}), 201 # You always have tu use jsonify to answer anything

# Login route
@app.route('/login', methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"Message": "That user is not in our database!"}), 401
    if password != user.password:
        return jsonify({"Message": "This password does not match our records regarding that user!"}), 401
    access_token = create_access_token(identity=email)
    return jsonify(Este_es_mi_token_de_acceso=access_token)

# Users routes

# Users list route 
@app.route('/user', methods=['GET'])
@jwt_required()
def say_hello():
    user = Users.query.all()
    list_of_users = list(map(lambda user: user.serialize(), user))
    response_body = {
        "Message": "Hello, this is the list of our users up till today!",
        "List of Users": list_of_users
    }
    return jsonify(response_body), 200

# "Providing User Info" route
@app.route('/user/<int:user_id>', methods=['GET'])
# @jwt_required()
def get_user(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    if user is None:
        response_body = {"Message": "There's no user with that user_id! Sorry!"}
        return jsonify(response_body), 404
    return jsonify(user.serialize()), 200

# Delete User
@app.route('/user/<int:user_id>', methods=['DELETE'])
# @jwt_required()
def delete_user(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    if user is None:
        response_body = {"Message": "There's no user with that user_id to delete! Sorry!"}
        return jsonify(response_body), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"Message": "User deleted successfully!"}), 200

# "List all characters" route
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    list_of_characters = list(map(lambda character: character.serialize(), characters))
    response_body = {
        "Message": "These are all the characters created up till now.",
        "List of Characters": list_of_characters
    }
    return jsonify(response_body), 200

# Delete character
@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Characters.query.filter_by(character_id=character_id).first()
    if character is None:
        response_body = {"Message": "There's no character with that character_id to delete! Sorry!"}
        return jsonify(response_body), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({"Message": "Character deleted successfully!"}), 200

# Get the information of one character
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.filter_by(character_id=character_id).first()
    return jsonify(character.serialize()), 200

# "List all planets" route
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    list_of_planets = list(map(lambda planet: planet.serialize(), planets))
    response_body = {
        "Message": "These are all the planets up till now!",
        "list_of_planets": list_of_planets
    }
    return jsonify(response_body), 200

# Get the information of one planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.filter_by(planet_id=planet_id).first()
    if planet is None:
        response_body = {"Message": "No planet to show!"}
        return jsonify(response_body), 404  
    return jsonify(planet.serialize()), 200

# Delete planet
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.filter_by(planet_id=planet_id).first()
    if planet is None:
        response_body = {"Message": "There's no planet with that planet_id to delete! Sorry!"}
        return jsonify(response_body), 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"Message": "Planet deleted successfully!"}), 200

# List all vehicles
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()
    list_of_vehicles = list(map(lambda vehicle: vehicle.serialize(), vehicles))
    response_body = {
        "Message": "These are all the vehicles up till now!",
        "list_of_vehicles": list_of_vehicles
    }
    return jsonify(response_body), 200

# Get the information of one vehicle
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicles.query.filter_by(vehicle_id=vehicle_id).first()
    if vehicle is None:
        response_body = {"Message": "No vehicle to be shown!"}
        return jsonify(response_body), 404  
    return jsonify(vehicle.serialize()), 200

# Delete vehicle
@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicles.query.filter_by(vehicle_id=vehicle_id).first()
    if vehicle is None:
        response_body = {"Message": "There's no vehicle with that character_id to delete! Sorry!"}
        return jsonify(response_body), 404
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"Message": "Vehicle deleted successfully!"}), 200

# Create character
@app.route('/characters', methods=['POST'])
def create_character():
    body = json.loads(request.data)
    check_character = Characters.query.filter_by(character_name=body["character_name"]).first()
    check_character_url = Characters.query.filter_by(character_url=body["character_url"]).first()
    if check_character_url:
        return jsonify({"Message": "A character with that URL already exists!"}), 400
    if not check_character:
        new_character = Characters(character_name=body["character_name"], character_url=body["character_url"])
        db.session.add(new_character)
        db.session.commit()
        return jsonify({"Message": "Character created successfully!"}), 201
    return jsonify({"Message": "A character with that name already exists!"}), 400

# Create planet
@app.route('/planets', methods=['POST'])
def create_planet():
    body = json.loads(request.data)
    check_planet = Planets.query.filter_by(planet_name=body["planet_name"]).first()
    check_planet_url = Planets.query.filter_by(planet_url=body["planet_url"]).first()
    if check_planet_url:
        return jsonify({"Message": "A planet with that URL already exists!"}), 400
    if not check_planet:
        new_planet = Planets(planet_name=body["planet_name"], planet_url=body["planet_url"])
        db.session.add(new_planet)
        db.session.commit()
        return jsonify({"Message": "Planet created successfully!"}), 201
    return jsonify({"Message": "A planet with that name already exists!"}), 400

# Create vehicle
@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    body = json.loads(request.data)
    check_vehicle = Vehicles.query.filter_by(vehicle_name=body["vehicle_name"]).first()
    check_vehicle_url = Vehicles.query.filter_by(vehicle_url=body["vehicle_url"]).first()
    if check_vehicle_url:
        return jsonify({"Message": "A vehicle with that URL already exists!"}), 400
    if not check_vehicle:
        new_vehicle = Vehicles(vehicle_name=body["vehicle_name"], vehicle_url=body["vehicle_url"])
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify({"Message": "vehicle created successfully!"}), 201
    return jsonify({"Message": "A vehicle with that name already exists!"}), 400

# Update character
@app.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    body = json.loads(request.data)
    character = Characters.query.filter_by(character_id=character_id).first()
    if character is None:
        response_body = {"Message": "No character to be updated!"}
        return jsonify(response_body), 404
    if "character_name" in body:
        character.character_name = body["character_name"]
    if "character_url" in body:
        character.character_url = body["character_url"]
    db.session.commit()
    return jsonify({"Message": "Character updated successfully!"}), 201

# Update planet
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    body = json.loads(request.data)
    planet = Planets.query.filter_by(planet_id=planet_id).first()
    if planet is None:
        response_body = {"Message": "No planet to be updated!"}
        return jsonify(response_body), 404
    if "planet_name" in body:
        planet.planet_name = body["planet_name"]
    if "planet_url" in body:
        planet.planet_url = body["planet_url"]
    db.session.commit()
    return jsonify({"Message": "Planet updated successfully!"}), 201

# Update vehicle
@app.route('/vehicle/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    body = json.loads(request.data)
    vehicle = Vehicles.query.filter_by(vehicle_id=vehicle_id).first()
    if vehicle is None:
        response_body = {"Message": "No vehicle to be updated!"}
        return jsonify(response_body), 404
    if "vehicle_name" in body:
        vehicle.vehicle_name = body["vehicle_name"]
    if "vehicle_url" in body:
        vehicle.vehicle_url = body["vehicle_url"]
    db.session.commit()
    return jsonify({"Message": "Vehicle updated successfully!"}), 201

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
# @jwt_required()
def get_user_favorites(user_id):
    # this_user_id = get_jwt_identity() # En principio habría de devolver el correo por la línea 75
    user_favorites = Favorites.query.filter_by(user_id=user_id).all()
    list_of_favorites = list(map(lambda favorites: favorites.serialize(), user_favorites))
    return jsonify(list_of_favorites), 200

@app.route('/user/<int:user_id>/favorites', methods=['POST'])
# @jwt_required()
def create_user_favorites(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    body = json.loads(request.data)
    if user is None:
        response_body = {"Message": "No user to add favorites to!"}
        return jsonify(response_body), 404
    favorite = Favorites.query.filter_by(user_id=user_id).first()
    if favorite is None:
        new_favorite = Favorites(user_id=user_id, character_id=body["character_id"], planets_id=body["planets_id"], vehicle_id=body["vehicle_id"])
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"Message": "Favorite added successfully!"}), 201
        

# DELETE

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)