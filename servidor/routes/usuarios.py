from flask import Blueprint, request, jsonify, render_template
from flask_mysqldb import MySQL
from app import app  # Importamos el objeto app de app.py

# Crear el Blueprint
usuarios_bp = Blueprint("usuarios", __name__)

# Ahora la conexión se maneja directamente con el contexto de Flask
mysql = MySQL(app)  # Usamos el objeto app global para inicializar mysql

@usuarios_bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios")
        usuarios = cur.fetchall()
        cur.close()
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({"error": str(e)})

@usuarios_bp.route("/usuarios", methods=['POST'])
def crear_usuario():
    try:
        datos = request.get_json()
        nombre = datos["nombre"]
        email = datos["email"]
        contraseña = datos["contraseña"]
        rol = datos["rol"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nombre, email, contraseña, rol) VALUES (%s, %s, %s, %s)", (nombre, email, contraseña, rol))
        mysql.connection.commit()
        cur.close()

        return jsonify({"mensaje": "Usuario creado con éxito"})
    except Exception as e:
        return jsonify({"error": str(e)})

