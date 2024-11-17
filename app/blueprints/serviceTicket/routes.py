from app.blueprints import serviceTicket
from .schemas import ServiceTicketSchema, MechanicSchema, CustomerSchema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import ServiceTicket, db
from sqlalchemy import select
from datetime import date
from app.utils.util import admin_required
from app.models import Mechanic
from flask import Blueprint
from app.blueprints.serviceTicket.schemas import serviceTickets_schema

serviceTicket_bp = serviceTicket.serviceTicket_bp

@serviceTicket_bp.route("/", methods=['POST'])
def create_new_serviceTicket():
    try:
        serviceTicket_data = ServiceTicketSchema().load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    mechanic_ids = serviceTicket_data.mechanics  
    serviceTicket_data.mechanics = []  

    for mechanic_id in mechanic_ids: 
        mechanic = Mechanic.query.get(mechanic_id)
        if mechanic:
            serviceTicket_data.mechanics.append(mechanic)
        else:
            return jsonify({"error": f"Mechanic with ID {mechanic_id} not found."}), 400

    db.session.add(serviceTicket_data)
    db.session.commit()

    return jsonify("New service ticket has been added to our database."), 201

@serviceTicket_bp.route("/all", methods=['GET'])
def get_all_serviceTickets():
    query = select(ServiceTicket)
    serviceTickets = db.session.execute(query).scalars().all()

    return ServiceTicketSchema(many=True).jsonify(serviceTickets), 200

@serviceTicket_bp.route("/<int:service_ticket_id>", methods=['GET'])
def get_service_ticket(service_ticket_id):
    serviceTicket = db.session.get(ServiceTicket, service_ticket_id)

    return ServiceTicketSchema().jsonify(serviceTicket), 200

@serviceTicket_bp.route("/<int:serviceTicket_id>", methods=['PUT'])
def update_service_ticket(serviceTicket_id):
    service_ticket = db.session.get(ServiceTicket, serviceTicket_id)

    if service_ticket == None:
        return jsonify({"message": "invalid id"}), 400

    try:
        serviceTicket_data = ServiceTicketSchema().load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in serviceTicket_data.items():
        if value:
            setattr(service_ticket, field, value)

    db.session.commit()
    return ServiceTicketSchema().jsonify(service_ticket), 200

@serviceTicket_bp.route("/<int:service_ticket_id>", methods=['DELETE'])
def delete_serviceTicket(service_ticket_id):
    serviceTicket = db.session.get(ServiceTicket, service_ticket_id)

    if serviceTicket == None:
        return jsonify({"message": "invalid id"}), 400

    db.session.delete(serviceTicket)
    db.session.commit()
    return jsonify({"message": f"Service ticket with ID {service_ticket_id} has been deleted"})
