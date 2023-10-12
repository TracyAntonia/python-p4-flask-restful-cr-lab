#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_list = [
            {
                "id": plant.id,
                "name": plant.name,
                "image": plant.image,
                "price": plant.price
            }
            for plant in plants
        ]
        return jsonify(plant_list)

    def post(self):
        data = request.get_json()
        name = data.get('name')
        image = data.get('image')
        price = data.get('price')

        if name and image and price:
            new_plant = Plant(name=name, image=image, price=price)
            db.session.add(new_plant)
            db.session.commit()
            return jsonify({
                "id": new_plant.id,
                "name": new_plant.name,
                "image": new_plant.image,
                "price": new_plant.price
            }, 201)
        return jsonify({"message": "Invalid data"}, 400)

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant:
            return jsonify({
                "id": plant.id,
                "name": plant.name,
                "image": plant.image,
                "price": plant.price
            })
        return jsonify({"message": "Plant not found"}, 404)

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
