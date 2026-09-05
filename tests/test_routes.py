"""Product service REST API routes."""
from flask import jsonify, request, abort
from service import app, db
from service.models import Product


@app.route("/products", methods=["POST"])
def create_product():
    product = Product().deserialize(request.get_json(force=True))
    product.create()
    return jsonify(product.serialize()), 201


@app.route("/products/<int:product_id>", methods=["GET"])
def read_product(product_id):
    """READ a single product"""
    product = Product.find(product_id)
    if not product:
        abort(404, f"Product {product_id} not found")
    return jsonify(product.serialize()), 200


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """UPDATE an existing product"""
    product = Product.find(product_id)
    if not product:
        abort(404, f"Product {product_id} not found")
    product.deserialize(request.get_json(force=True))
    product.id = product_id
    product.update()
    return jsonify(product.serialize()), 200


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """DELETE a product"""
    product = Product.find(product_id)
    if not product:
        abort(404, f"Product {product_id} not found")
    product.delete()
    return jsonify({"message": "deleted"}), 200


@app.route("/products", methods=["GET"])
def list_products():
    """LIST ALL, LIST BY NAME, LIST BY CATEGORY, LIST BY AVAILABILITY"""
    name = request.args.get("name")
    category = request.args.get("category")
    availability = request.args.get("availability")

    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(category)
    elif availability is not None:
        products = Product.find_by_availability(availability.lower() == "true")
    else:
        products = Product.all()

    return jsonify([p.serialize() for p in products]), 200


@app.route("/", methods=["GET"])
def index():
    return jsonify({"service": "product-catalog", "status": "running"}), 200


with app.app_context():
    db.create_all()
