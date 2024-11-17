from app.models import Mechanic
from app.extensions import ma



class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        include_fk = True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
login_mechanic_schema = MechanicSchema(exclude=["salary", "phone" ])