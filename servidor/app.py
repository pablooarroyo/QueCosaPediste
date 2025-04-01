from flask import Flask, render_template
from flask_cors import CORS
from config import Config # Asegúrate de que este archivo existe y está bien configurado
import os

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar MySQL y CORS
CORS(app)

# Ahora registramos el blueprint después de la configuración de Flask
if __name__ == "__main__":
    # Importar las rutas dentro del bloque `if` para evitar importación circular
    from routes.usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp)  # Prefijo de /api para las rutas

    @app.route("/")
    def home():
        return render_template("index.html")

    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

