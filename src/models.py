from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(80), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='users', lazy=True)

    def __repr__(self):
        return '<Users %r>' % self.user_email

    def serialize(self):
        return {
            "User ID": self.user_id,
            "User Email": self.user_email,
            # Do not serialize the password (It is a security breach!)
        }

class Characters(db.Model):
    character_id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(120), nullable=False)
    character_url = db.Column(db.String(250), unique=True, nullable=False)
    favorites = db.relationship('Favorites', backref='characters', lazy=True)

    def __repr__(self):
        return '<Characters %r>' % self.character_name

    def serialize(self):
        return {
            "Character ID": self.character_id,
            "Character Name": self.character_name,
            "Character URL": self.character_url,
        }

class Planets(db.Model):
    planet_id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(120), nullable=False)
    planet_url = db.Column(db.String(250), unique=True, nullable=False)
    favorites = db.relationship('Favorites', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.planet_name

    def serialize(self):
        return {
            "Planet ID": self.planet_id,
            "Planet Name": self.planet_name,
            "Planet URL": self.planet_url,
        }

class Vehicles(db.Model):
    vehicle_id = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(120), nullable=False)
    vehicle_url = db.Column(db.String(250), unique=True, nullable=False)
    favorites = db.relationship('Favorites', backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicles %r>' % self.vehicle_name

    def serialize(self):
        return {
            "Vehicle ID": self.vehicle_id,
            "Vehicle Name": self.vehicle_name,
            "Vehicle URL": self.vehicle_url,
        }

class Favorites(db.Model):
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), unique=True, nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey("characters.character_id"), unique=True, nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.planet_id"), unique=True, nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.vehicle_id"), unique=True, nullable=True)

    def __repr__(self):
        return '<Favorites %r>' % self.favorite_id

    def serialize(self):
        return {
            "favorite id": self.favorite_id,
            "user_id": self.user_id,
            "people_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id,
        }