import mysql.connector
# configuramos la conexion
def conectar_BBDD():
    try:
        conn= mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="QueCosaPediste"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar: {err}")
        return None