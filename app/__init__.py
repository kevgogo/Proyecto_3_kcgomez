from flask import Flask
from config import Config
from app.extensions import db, bcrypt
from app.utils import conditional_print

def create_app():
    """
    Configura y retorna la aplicación Flask con extensiones y rutas registradas.
    """
    # Crear instancia de la aplicación Flask
    app = Flask(__name__)
    app.config.from_object(Config)

    app.secret_key = Config.SECRET_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.database_uri()
    conditional_print(f"Final SQLALCHEMY_DATABASE_URI: {Config.database_uri()}")
    
    # Inicializar extensiones
    db.init_app(app)
    conditional_print("SQLAlchemy initialized successfully.")

    bcrypt.init_app(app)
    conditional_print("BCrypt initialized successfully.")

    with app.app_context():
        from app.api_routes import registrar_rutas_api
        from app.web_routes import registrar_rutas_web

        registrar_rutas_api(app)
        registrar_rutas_web(app)
    
        from app.data_loader import inicializar_base_de_datos
        inicializar_base_de_datos()

    return app