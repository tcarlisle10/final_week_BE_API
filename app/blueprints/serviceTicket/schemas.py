from app.models import ServiceTicket, Mechanic, Customer
from app.extensions import ma
from marshmallow import fields
from app.blueprints.mechanic.schemas import MechanicSchema
from app.blueprints.customer.schemas import CustomerSchema


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True  
        include_relationships = True
        load_instance = True

    
    customer_id = fields.Integer(required=True)
    mechanic_ids = fields.List(fields.Integer(), required=True, load_only=True)

    
    customer = fields.Nested('CustomerSchema', only=['id', 'name'], dump_only=True)
    mechanics = fields.List(fields.Nested('MechanicSchema', only=['id', 'name']), dump_only=True)


serviceTicket_schema = ServiceTicketSchema()
serviceTickets_schema = ServiceTicketSchema(many=True)


