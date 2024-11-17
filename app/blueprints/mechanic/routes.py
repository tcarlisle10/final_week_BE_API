from app.blueprints import mechanic
from .schemas import mechanic_schema, mechanics_schema
from app.blueprints.serviceTicket.schemas import serviceTickets_schema
from flask import request, jsonify, abort
from marshmallow import ValidationError
from app.models import Mechanic, db
from sqlalchemy import select
from app.utils.util import encode_token, token_required
from werkzeug.security import generate_password_hash, check_password_hash

mechanic_bp = mechanic.mechanic_bp

@mechanic_bp.route("/create", methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = request.json
        mechanic_data = mechanic_schema.load(mechanic_data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    pwhash = generate_password_hash(mechanic_data['password'])
    new_mechanic = Mechanic(
        name=mechanic_data['name'],
        email=mechanic_data['email'],
        phone=mechanic_data['phone'],
        password=pwhash,
        role=mechanic_data['role'], 
        salary=mechanic_data['salary']  
    )
    db.session.add(new_mechanic)
    db.session.commit()

    return jsonify("Mechanic has been added to our database."), 201

@mechanic_bp.route("/login", methods=['POST'])
def login_mechanic():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        mechanic = Mechanic.query.filter_by(email=email).first()

        if not mechanic or not check_password_hash(mechanic.password, password):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        token = encode_token(mechanic.id)
        return jsonify({'token': token, 'message': 'Login successful'}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred'}), 500

@mechanic_bp.route("/", methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()

    return mechanics_schema.jsonify(mechanics), 200

@mechanic_bp.route("/<int:mechanic_id>", methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if mechanic is None:
        abort(404, description=f"Mechanic with ID {mechanic_id} not found.")

    return mechanic_schema.jsonify(mechanic), 200

@mechanic_bp.route("/<int:mechanic_id>", methods=['PUT'])
@token_required
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if mechanic is None:
        abort(404, description=f"Mechanic with ID {mechanic_id} not found.")

    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in mechanic_data.items():
        if value:
            setattr(mechanic, field, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@mechanic_bp.route("/<int:mechanic_id>", methods=['DELETE'])
@token_required
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if mechanic is None:
        abort(404, description=f"Mechanic with ID {mechanic_id} not found.")

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic with ID {mechanic_id} has been deleted."}), 200

@mechanic_bp.route("/<int:mechanic_id>/tickets", methods=['GET'])
def get_mechanic_tickets(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic is None:
        abort(404, description=f"Mechanic with ID {mechanic_id} not found.")

    tickets = mechanic.serviceTickets  

    return serviceTickets_schema.jsonify(tickets), 200

@mechanic_bp.route("/<int:mechanic_id>/tickets/<int:ticket_id>", methods=['PUT'])
@token_required
def update_service_ticket(mechanic_id, ticket_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic is None:
        abort(404, description=f"Mechanic with ID {mechanic_id} not found.")

    if mechanic.role != 'admin':
        return jsonify({"message": "Admin role required"}), 403

    ticket = next((t for t in mechanic.serviceTickets if t.id == ticket_id), None)
    if ticket is None:
        abort(404, description=f"Service ticket with ID {ticket_id} not found.")

    try:
        ticket_data = serviceTickets_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in ticket_data.items():
        if value:
            setattr(ticket, field, value)

    db.session.commit()
    return serviceTickets_schema.jsonify(ticket), 200

@mechanic_bp.route("/<int:mechanic_id>/tickets/<int:ticket_id>", methods=['DELETE'])
@token_required
def delete_service_ticket(mechanic_id, ticket_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic is None:
        abort(404, description=f"Mechanic with ID {mechanic_id} not found.")

    if mechanic.role != 'admin':
        return jsonify({"message": "Admin role required"}), 403

    ticket = next((t for t in mechanic.serviceTickets if t.id == ticket_id), None)
    if ticket is None:
        abort(404, description=f"Service ticket with ID {ticket_id} not found.")

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Service ticket with ID {ticket_id} has been deleted."}), 200
