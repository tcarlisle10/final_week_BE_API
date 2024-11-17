from app.models import Customer
from app.extensions import ma
from marshmallow import fields


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
    # serviceTickets = fields.Nested("ServiceTicketSchema", many=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
# login_schema = CustomerSchema(exclude=["phone", "name", "role"])