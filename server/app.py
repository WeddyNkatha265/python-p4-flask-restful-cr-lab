#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        response_dict = [plant.to_dict() for plant in plants]
        response = make_response(jsonify(response_dict), 200)
        return response

    def post(self):
        try:
            new_plant = Plant(
                image=request.json['image'], 
                name=request.json['name'],
                price=request.json['price'],
            )
            db.session.add(new_plant)
            db.session.commit()
            response_dict = new_plant.to_dict()
            response = make_response(jsonify(response_dict), 201)
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify({"error": str(e)}), 400)
        return response

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            response_dict = plant.to_dict()
            response = make_response(jsonify(response_dict), 200)
        else:
            response = make_response(jsonify({"error": "Plant not found"}), 404)
        return response

api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
