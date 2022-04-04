from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


""" association_table = db.Table('favorites', db.Model.metadata,
    db.Column('user_id', db.ForeignKey('user.id')),
    db.Column('people_id', db.ForeignKey('people.id')),
    db.Column('planets_id', db.ForeignKey('planets.id')),
    db.Column('vehicles_id', db.ForeignKey('vehicles.id'))
) """

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    fav_people = db.relationship('FavoritePeople', lazy=True)
    fav_planets = db.relationship('FavoritePlanets', lazy=True)
    """ people = db.relationship("People", 
                            secondary=association_table)
    planets = db.relationship("Planets", 
                            secondary=association_table)
    vehicles = db.relationship("Vehicles", 
                            secondary=association_table) """

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    birth_year = db.Column(db.String(20))
    eye_color = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    height = db.Column(db.Integer)
    homeworld = db.Column(db.String(100))
    mass = db.Column(db.Integer)
    skin_color = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship(User)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "height": self.height,
            "homeworld": self.homeworld,
            "mass": self.mass,
            "skin_color": self.skin_color
        }

class FavoritePeople(db.Model):
    __tablename__ = 'favorite_people'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<FavoritePeople %r>' % self.people_id

    def serialize(self):
        return {
            "planets_id": self.people_id
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    climate = db.Column(db.String(20))
    diameter = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship(User)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "population": self.population,
            "terrain": self.terrain
        }

class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planets_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<FavoritePlanets %r>' % self.planets_id

    def serialize(self):
        return {
            "planets_id": self.planet_id
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    cargo_capacity = db.Column(db.Integer)
    consumables = db.Column(db.String(50), nullable=False)
    cost_in_credits = db.Column(db.Integer, nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    hyperdrive_rating = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "cost_in_credits": self.cost_in_credits,
            "crew": self.crew,
            "hyperdrive_rating": self.hyperdrive_rating,
            "manufacturer": self.manufacturer,
            "model": self.model
        }