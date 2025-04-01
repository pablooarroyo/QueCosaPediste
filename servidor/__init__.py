from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from .config import Config  # Asegúrate de tener este archivo en la misma carpeta

# Inicializamos MySQL y CORS
mysql = MySQL()
cors = CORS()

def create_app():
    app = Flask(__name__)
    
    # Cargar la configuración desde el archivo Config
    app.config.from_object(Config)
    
    # Inicializar MySQL y CORS
    mysql.init_app(app)
    cors.init_app(app)
    
    # Registramos el Blueprint de usuarios
    from .routes.usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api')  # Prefijo /api para las rutas
    
    # Agregamos una ruta simple para verificar el servidor
    @app.route("/")
    def home():
        return {"mensaje": "Servidor funcionando 🚀"}
    
    return app
