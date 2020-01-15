
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.squlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init SqlAlchemy DB
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)


# Product Class/model
class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price", "qty")


# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a Product
@app.route("/product", methods=["POST"])
def add_product():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# print
@app.route("/print", methods=["GET"])
def print_test():
    return ("PRINTANDO UAU BLABLA <br> BLA <br> all your base are belong to us")

# Get all products
@app.route("/count", methods=["GET"])
def get_count():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    array_json = jsonify(result)
    array_json = result
    result = 0
    for i in array_json:
        result += 1
    return str(result)

# Get all products
@app.route("/product", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Get single products
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Update Product
@app.route("/product/<id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)

    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product)

# Delete
@app.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Run Server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)