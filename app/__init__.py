from flask import Flask
from app.models import db
from app.extensions import ma, Cache, Limiter  # Import the Limiter extension
from app.blueprints.customer import customer_bp
from app.blueprints.mechanic import mechanic_bp
from app.blueprints.serviceTicket import serviceTicket_bp
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restx import Api

SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI (without trailing '/')
API_URL = "/static/swagger.yaml"  

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Mechanic API"}
)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")
    
    api = Api(app)  

    app.register_blueprint(customer_bp, url_prefix="/customer")
    app.register_blueprint(serviceTicket_bp, url_prefix="/serviceTicket")
    app.register_blueprint(mechanic_bp, url_prefix="/mechanic")
    app.register_blueprint(swagger_bp)

    db.init_app(app)
    ma.init_app(app)
    Cache.init_app(app)

    my_limiter = Limiter(  # Create the limiter object
        key_func=get_remote_address, default_limits=["200 per day", "50 per hour"]
    )

    my_limiter.init_app(app)  # Initialize the extension with your limiter

    return app