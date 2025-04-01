from flask import Blueprint, request, jsonify, render_template
import mysql.connector
import os

usuarios_bp = Blueprint("usuarios", __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

@usuarios_bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios")
        usuarios = cur.fetchall()
        cur.close()
        conn.close()
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

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (nombre, email, contraseña, rol) VALUES (%s, %s, %s, %s)",
                    (nombre, email, contraseña, rol))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"mensaje": "Usuario creado con éxito"})
    except Exception as e:
        return jsonify({"error": str(e)})

