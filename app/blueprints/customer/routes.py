from app.blueprints import customer
from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customer, db
from sqlalchemy import select
from app.utils.util import encode_token, token_required
from werkzeug.security import generate_password_hash, check_password_hash

customer_bp = customer.customer_bp
@customer_bp.route("/", methods=['POST'])
def create_customer():
    try: 
        customer_data = request.json
        print(f"Received customer data: {customer_data}")
        customer_data = customer_schema.load(customer_data) 
        print(f"Validated customer data: {customer_data}")
    except ValidationError as e:
        print(f"Validation Error: {e.messages}")
        return jsonify(e.messages), 400
    
    pwhash = generate_password_hash(customer_data['password'])
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'], password=pwhash)
    db.session.add(new_customer) 
    db.session.commit() 

    return jsonify("Customer has been added our database."), 201


@customer_bp.route("/all", methods=['GET'])
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    
    return customers_schema.jsonify(customers), 200


@customer_bp.route("/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    return customer_schema.jsonify(customer), 200


@customer_bp.route("/<int:customer_id>", methods=['PUT'])
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer == None:
        return jsonify({"message": "invalid id"}), 400
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        print(f"Validation Error: {e.messages}")
        return jsonify(e.messages), 400
    
    for field, value in customer_data.items():
        if value:
            setattr(customer, field, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200


@customer_bp.route("/<int:customer_id>", methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer == None:
        return jsonify({"message": "invalid id"}), 400

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"User at ID {customer_id} has been deleted "})

