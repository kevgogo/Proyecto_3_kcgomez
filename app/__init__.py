from flask import Flask
from config import Config
from app.extensions import initialize_extensions
from app.api_routes import api
from app.web_routes import web

def create_app():
    """
    Configura y retorna la aplicación Flask con extensiones y rutas registradas.
    """
    # Crear instancia de la aplicación Flask
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)

    app.secret_key = Config.SECRET_KEY
    app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.database_uri()
    Config.conditional_print(f"Final SQLALCHEMY_DATABASE_URI: {Config.database_uri()}")
    
    # Inicializar extensiones
    initialize_extensions(app)

    with app.app_context():
        app.register_blueprint(api) # Para la API
        Config.conditional_print("Api Blueprint Registered successfully.")
        app.register_blueprint(web) # Para la Heladeria
        Config.conditional_print("Web Blueprint Registered successfully.")

        from app.data_loader import inicializar_base_de_datos
        inicializar_base_de_datos()

    return app