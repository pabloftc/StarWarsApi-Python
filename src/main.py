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
from models import db, User, People, Planets, Vehicles
from models import FavoritePeople, FavoritePlanets
#from models import Person

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

@app.route('/users', methods=['GET'])
def handle_hello():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/users/favorites', methods=['GET'])
def handle_user_favorites():

    user_id = request.args.get("user_id")
    
    fav_people = FavoritePeople.query.filter_by(user_id=user_id)
    fav_people_list = list(map(lambda x: x.serialize(), fav_people))

    fav_planets = FavoritePlanets.query.filter_by(user_id=user_id)
    fav_planets_list = list(map(lambda x: x.serialize(), fav_planets))

    favorite_list = {
        "favorite people": fav_people_list,
        "favorite planets": fav_planets_list
    }

    return jsonify(favorite_list), 200

@app.route('/people', methods=['GET'])
def handle_people():

    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people))

    return jsonify(all_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_one_people(people_id):

    one_people = People.query.get(people_id)

    return jsonify(one_people), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people(people_id):

    user_id = request.args.get("user_id")
    fav_people = FavoritePeople(user_id, people_id)
    db.session.add(fav_people)
    db.session.commit()

    return "Added people to favorites", 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def add_people(people_id):

    user_id = request.args.get("user_id")
    fav_people = FavoritePeople(user_id, people_id)
    db.session.delete(fav_people)
    db.session.commit()

    return "Deleted people from favorites", 200

@app.route('/planets', methods=['GET'])
def handle_planets():

    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))

    return jsonify(all_planets), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def handle_one_planet(planets_id):

    one_planet = Planets.query.get(planets_id)

    return jsonify(one_planet), 200

@app.route('/favorite/planets/<int:planets_id>', methods=['POST'])
def add_planets(planets_id):

    user_id = request.args.get("user_id")
    fav_planets = FavoritePlanets(user_id, planets_id)
    db.session.add(fav_planets)
    db.session.commit()

    return "Added planet to favorites", 200

@app.route('/favorite/planets/<int:planets_id>', methods=['DELETE'])
def add_planets(planets_id):

    user_id = request.args.get("user_id")
    fav_planets = FavoritePlanets(user_id, planets_id)
    db.session.delete(fav_planets)
    db.session.commit()

    return "Deleted planet from favorites", 200
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
