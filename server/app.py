#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants')
def restaurants():
    rest = [{"address": restaurant.address, "id": restaurant.id, "name": restaurant.name} for restaurant in Restaurant.query.all()]
    
    response = make_response(
        rest, 
        200
    )
    return response 

@app.route('/restaurants/<int:id>', methods=["GET", "DELETE"])
def restaurant_by_id(id):
    rest =  Restaurant.query.filter(Restaurant.id == id).first()
    if request.method == "GET":
        if rest:
            rest_dict = rest.to_dict()

            response = make_response(
                rest_dict,
                200
            )
            return response
        elif not rest:
            response = make_response(
                {"error": "Restaurant not found"}, 404
            )
            return response 
    elif request.method == "DELETE":
        db.session.delete(rest)
        db.session.commit()
        response = make_response(
            {},
            204
        )
        return response 
    
@app.route('/pizzas')
def pizzas():
    pizza_list = [{"id": pizza.id, "ingredients": pizza.ingredients, "name": pizza.name} for pizza in Pizza.query.all()]
    
    response = make_response(
        pizza_list, 
        200
    )
    return response

@app.route('/restaurant_pizzas', methods=["POST"])
def restaurant_pizzas(): 
    if request.method == "POST":
        data = request.get_json()
        price = data.get('price')
        pizza_id = data.get('pizza_id')
        restaurant_id = data.get('restaurant_id')
        
        try:
            restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
            db.session.add(restaurant_pizza)
            db.session.commit()
            return make_response(
                restaurant_pizza.to_dict(), 201
            )
        except Exception:
            return make_response({"errors": ["validation errors"]}, 400)
    

if __name__ == "__main__":
    app.run(port=5555, debug=True)
