import mysql
from BBDD import conectar_BBDD

#VERIFICAR SI EL USUARIO EXISTE

def usuario_existe(email):
    """ Verifica si un usuario ya está registrado por su email """
    conn = conectar_BBDD()
    if not conn:
        return False

    cursor = conn.cursor()
    query = "SELECT id_usuario FROM Usuarios WHERE email = %s"
    cursor.execute(query, (email,))
    usuario = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return usuario is not None  # Retorna True si el usuario existe


#REGISTRARSE

def registrar_usuario(nombre, email, contraseña, telefono, rol):
    """ Registra un nuevo usuario si no está ya registrado """
    if usuario_existe(email):
        print("⚠ El usuario ya está registrado. ¿Quieres iniciar sesión? (Sí/No)")
        opcion = input().strip().lower()
        if opcion == "sí" or opcion == "si":
            return "login"  # Indicamos que el usuario quiere iniciar sesión
        return None

    conn = conectar_BBDD()
    if not conn:
        return "Error de conexión"

    cursor = conn.cursor()

    try:
        # Insertar en la tabla Usuarios
        query = "INSERT INTO Usuarios (nombre, email, contraseña, telefono, rol) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre, email, contraseña, telefono, rol)
        cursor.execute(query, valores)
        id_usuario = cursor.lastrowid  # Obtener el ID del usuario recién creado

        # Insertar en la tabla correspondiente según el rol
        if rol == "cliente":
            cursor.execute("INSERT INTO clientes (id_usuario, direccion, metodo_pago) VALUES (%s, '', '')", (id_usuario,))
        elif rol == "restaurante":
            cursor.execute("INSERT INTO restaurantes (id_usuario, nombre_comercial, direccion, telefono_contacto) VALUES (%s, '', '', '')", (id_usuario,))
        elif rol == "repartidor":
            cursor.execute("INSERT INTO repartidores (id_usuario, vehiculo, licencia_conduccion) VALUES (%s, '', '')", (id_usuario,))

        conn.commit()
        print("✅ Usuario registrado correctamente y añadido a su tabla correspondiente.")
    except mysql.connector.Error as err:
        print(f"⚠ Error: {err}")
    finally:
        cursor.close()
        conn.close()

#LOGIN

def login_usuario(email, contraseña):
    """ Verifica si el usuario existe y la contraseña es correcta """
    conn = conectar_BBDD()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Usuarios WHERE email = %s AND contraseña = %s"
    cursor.execute(query, (email, contraseña))
    usuario = cursor.fetchone()  # Obtiene el usuario si existe

    cursor.close()
    conn.close()

    if usuario:
        print(f"✅ Login exitoso. Bienvenido {usuario['nombre']} ({usuario['rol']}).")
        return usuario  # Retorna los datos del usuario si el login es correcto
    else:
        print("⚠ Usuario o contraseña incorrectos.")
        return None

#ELIMINAR USUARIOS

def eliminar_usuario(email):
    """ Elimina un usuario por su email si existe """
    conn = conectar_BBDD()
    if not conn:
        return "❌ Error de conexión"

    cursor = conn.cursor()

    # Verificar si el usuario existe
    cursor.execute("SELECT id_usuario FROM Usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()

    if not usuario:
        print("⚠ No existe un usuario con ese email.")
        return

    id_usuario = usuario[0]

    try:
        # Eliminar usuario (y por ON DELETE CASCADE también se eliminará de clientes, restaurantes o repartidores)
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        print("✅ Usuario eliminado correctamente.")
    except mysql.connector.Error as err:
        print(f"⚠ Error al eliminar usuario: {err}")
    finally:
        cursor.close()
        conn.close()

#MENU RESTAURANTE

def menu_restaurante(usuario):
    print(f"\n🍽️ Bienvenido, {usuario['nombre']} (Restaurante)")
    print("1️⃣ Configurar información del restaurante")
    print("2️⃣ Añadir/editar menú")
    print("3️⃣ Ver pedidos recibidos")
    print("4️⃣ Ver reseñas de clientes")
    print("5️⃣ Salir")
    opcion = input("Elige una opción: ")
    
    if opcion == "1":
        configurar_restaurante(usuario)
    elif opcion == "2":
        gestionar_menu(usuario)
    elif opcion == "3":
        ver_pedidos_restaurante(usuario)
    elif opcion == "4":
        ver_reseñas_restaurante(usuario)
    elif opcion == "5":
            print("🔙 Volviendo al menú principal...")
            return False  # Indica que el usuario quiere salir al menú principal
    else:
        print("Saliendo...")

#MENU REPARTIDOR

def menu_repartidor(usuario):
    """ Menú para repartidores """
    while True:
        print(f"\n🚴 Bienvenido, {usuario['nombre']} (Repartidor)")
        print("1️⃣ Activar/Desactivar disponibilidad")
        print("2️⃣ Ver pedidos asignados")
        print("3️⃣ Marcar pedido como entregado")
        print("4️⃣ Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            cambiar_disponibilidad(usuario)

        elif opcion == "2":
            ver_pedidos_repartidor(usuario)

        elif opcion == "3":
            id_pedido = input("Ingrese el ID del pedido que ha sido entregado: ")
            marcar_pedido_entregado(usuario, id_pedido)

        elif opcion == "4":
            print("🔙 Volviendo al menú principal...")
            return False  # Indica que el usuario quiere salir al menú principal

        else:
            print("⚠ Opción no válida. Inténtalo de nuevo.")


#MENU CLIENTE

def menu_cliente(usuario):
    print(f"\n👤 Bienvenido, {usuario['nombre']} (Cliente)")
    print("1️⃣ Ver restaurantes disponibles")
    print("2️⃣ Hacer un pedido")
    print("3️⃣ Ver historial de pedidos")
    print("4️⃣ Calificar un pedido entregado")
    print("5️⃣ Salir")
    opcion = input("Elige una opción: ")
    
    if opcion == "1":
        ver_restaurantes()
    elif opcion == "2":
        hacer_pedido(usuario)
    elif opcion == "3":
        ver_historial_pedidos(usuario)
    elif opcion == "4":
        opinar_sobre_pedido(usuario)
    elif opcion == "5":
            print("🔙 Volviendo al menú principal...")
            return False  # Indica que el usuario quiere salir al menú principal
    else:
            print("⚠ Opción no válida. Inténtalo de nuevo.")

# CONFIGURAR RESTAURANTE

def configurar_restaurante(usuario):
    """ Permite a un restaurante actualizar su información """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor()
    nombre_comercial = input("Nombre del restaurante: ")
    direccion = input("Ubicación: ")
    telefono_contacto = input("Teléfono de contacto: ")

    try:
        query = "UPDATE restaurantes SET nombre_comercial=%s, direccion=%s, telefono_contacto=%s WHERE id_usuario=%s"
        valores = (nombre_comercial, direccion, telefono_contacto, usuario["id_usuario"])
        cursor.execute(query, valores)
        conn.commit()
        print("✅ Información del restaurante actualizada.")
    except mysql.connector.Error as err:
        print(f"⚠ Error: {err}")
    finally:
        cursor.close()
        conn.close()

#GESTIONAR EL MENÚ DEL RESTAURANTE

def gestionar_menu(usuario):
    """ Permite a un restaurante añadir platos a su menú """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor()
    nombre_plato = input("Nombre del plato: ")
    descripcion = input("Descripción: ")
    precio = input("Precio: ")

    try:
        query = "INSERT INTO platos (id_restaurante, nombre, descripcion, precio, disponible) VALUES ((SELECT id_restaurante FROM restaurantes WHERE id_usuario=%s), %s, %s, %s, TRUE)"
        valores = (usuario["id_usuario"], nombre_plato, descripcion, precio)
        cursor.execute(query, valores)
        conn.commit()
        print("✅ Plato añadido al menú.")
    except mysql.connector.Error as err:
        print(f"⚠ Error: {err}")
    finally:
        cursor.close()
        conn.close()

#DISPONIBILIDAD DEL REPARTIDOR

def cambiar_disponibilidad(usuario):
    """ Permite a un repartidor cambiar su estado de disponibilidad """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor()
    estado = input("¿Quieres estar disponible para recibir pedidos? (Sí/No): ").strip().lower()
    disponible = 1 if estado in ["sí", "si"] else 0

    try:
        # Actualizar estado de disponibilidad
        cursor.execute("UPDATE repartidores SET disponible=%s WHERE id_usuario=%s", (disponible, usuario["id_usuario"]))
        conn.commit()
        print("✅ Estado actualizado.")

        # Si ahora está disponible → revisar pedidos pendientes sin repartidor
        if disponible:
            cursor.execute("""
                SELECT p.id_pedido 
                FROM pedidos p
                LEFT JOIN reparto_pedidos r ON p.id_pedido = r.id_pedido
                WHERE p.estado = 'pendiente' AND r.id_pedido IS NULL
                ORDER BY p.fecha_pedido ASC LIMIT 1
            """)
            pedido = cursor.fetchone()

            if pedido:
                id_pedido = pedido[0]

                # Obtener id_repartidor actual
                cursor.execute("SELECT id_repartidor FROM repartidores WHERE id_usuario=%s", (usuario["id_usuario"],))
                repartidor = cursor.fetchone()
                id_repartidor = repartidor[0]

                # Asignar el pedido
                cursor.execute("""
                INSERT INTO reparto_pedidos (id_pedido, id_repartidor, estado) 
                VALUES (%s, %s, 'en camino')
                """, (id_pedido, id_repartidor))

                # Cambiar estado del pedido
                cursor.execute("UPDATE pedidos SET estado = 'en camino' WHERE id_pedido = %s", (id_pedido,))

                # Enviar notificación
                cursor.execute("""
                INSERT INTO notificaciones (id_usuario, mensaje)
                VALUES (%s, %s)
                """, (usuario["id_usuario"], f"Se te ha asignado el pedido pendiente (ID: {id_pedido}). ¡Revisa tu app!"))

                # Marcar como ocupado
                cursor.execute("UPDATE repartidores SET disponible = FALSE WHERE id_usuario = %s", (usuario["id_usuario"],))

                conn.commit()
                print(f"✅ Se te asignó automáticamente el pedido {id_pedido}.")

            else:
                print("ℹ️ No hay pedidos pendientes por asignar.")

    except mysql.connector.Error as err:
        print(f"⚠ Error: {err}")
    finally:
        cursor.close()
        conn.close()


#VER LOS RESTAURANTES DISPONIBLES

def ver_restaurantes():
    """ Muestra los restaurantes y permite ver sus reseñas si se desea """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
        SELECT r.id_restaurante, r.nombre_comercial, r.direccion,
               ROUND(AVG(re.calificación), 1) AS promedio,
               COUNT(re.id_reseña) AS cantidad
        FROM restaurantes r
        LEFT JOIN resenyas re ON r.id_restaurante = re.id_restaurante
        GROUP BY r.id_restaurante
        """)
        restaurantes = cursor.fetchall()

        if not restaurantes:
            print("⚠ No hay restaurantes disponibles.")
            return

        print("\n📍 Restaurantes disponibles:")
        for r in restaurantes:
            calif = f"{r['promedio']}⭐ ({r['cantidad']} reseñas)" if r['cantidad'] else "Sin reseñas aún"
            print(f"🆔 {r['id_restaurante']} | 🍽️ {r['nombre_comercial']} - {r['direccion']} | {calif}")

        opcion = input("\n¿Quieres ver las reseñas de algún restaurante? Ingresa el ID o 'no': ").strip().lower()

        if opcion.isdigit():
            ver_reseñas_de_restaurante(int(opcion))
        elif opcion in ['no', 'n']:
            print("🔙 Volviendo al menú del cliente.")
        else:
            print("⚠ Opción no válida.")

    except mysql.connector.Error as err:
        print(f"⚠ Error: {err}")
    finally:
        cursor.close()
        conn.close()


#HACER UN PEDIDO 

def hacer_pedido(usuario):
    """ Permite a un cliente hacer un pedido con una dirección de entrega """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)

    # Mostrar restaurantes disponibles
    ver_restaurantes()
    id_restaurante = input("Elige el ID del restaurante: ")

    # Mostrar menú del restaurante
    cursor.execute("SELECT id_plato, nombre, precio FROM platos WHERE id_restaurante=%s AND disponible=TRUE", (id_restaurante,))
    platos = cursor.fetchall()

    if not platos:
        print("⚠ Este restaurante no tiene platos disponibles.")
        return

    print("\n📜 Menú:")
    for p in platos:
        print(f"{p['id_plato']} - {p['nombre']} (${p['precio']})")

    # Elegir platos
    id_plato = input("Elige el ID del plato: ")
    cantidad = int(input("Cantidad: "))
    
    # Pedir la dirección de entrega
    direccion_entrega = input("📍 Ingresa la dirección de entrega: ")

    try:
        # Crear el pedido en la base de datos
        query = """
        INSERT INTO pedidos (id_cliente, id_restaurante, estado, total, direccion_entrega) 
        VALUES ((SELECT id_cliente FROM clientes WHERE id_usuario=%s), %s, 'pendiente', 
        (SELECT precio FROM platos WHERE id_plato=%s) * %s, %s)
        """
        valores = (usuario["id_usuario"], id_restaurante, id_plato, cantidad, direccion_entrega)
        cursor.execute(query, valores)
        id_pedido = cursor.lastrowid  # Obtener el ID del pedido recién creado
        conn.commit()

        print(f"✅ Pedido {id_pedido} realizado con éxito. Dirección de entrega: {direccion_entrega}")

        # Enviar notificación al restaurante (implementaremos después)
        # notificar_restaurante(id_restaurante, id_pedido)

        # Intentar asignar el pedido a un repartidor disponible
        asignar_pedido_a_repartidor(id_pedido)

    except mysql.connector.Error as err:
        print(f"⚠ Error: {err}")

    finally:
        cursor.close()
        conn.close()

#VER HISTORIAL PEDIDOS

def ver_historial_pedidos(usuario):
    """ Muestra el historial de pedidos de un cliente """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT p.id_pedido, p.fecha_pedido, p.total, p.estado, r.nombre_comercial 
    FROM pedidos p
    JOIN restaurantes r ON p.id_restaurante = r.id_restaurante
    WHERE p.id_cliente = (SELECT id_cliente FROM clientes WHERE id_usuario=%s)
    """
    cursor.execute(query, (usuario["id_usuario"],))
    pedidos = cursor.fetchall()

    if pedidos:
        print("\n📜 Historial de Pedidos:")
        for p in pedidos:
            print(f"🆔 Pedido {p['id_pedido']} | Restaurante: {p['nombre_comercial']} | Total: ${p['total']} | Estado: {p['estado']} | Fecha: {p['fecha_pedido']}")
    else:
        print("⚠ No tienes pedidos anteriores.")

    cursor.close()
    conn.close()

#VER PEDIDOS RESTAURANTE

def ver_pedidos_restaurante(usuario):
    """ Muestra los pedidos recibidos por un restaurante con la dirección de entrega """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        SELECT p.id_pedido, usuarios.nombre AS cliente, usuarios.telefono, usuarios.email, 
               p.total, p.estado, p.fecha_pedido, p.direccion_entrega
        FROM pedidos p
        JOIN clientes ON p.id_cliente = clientes.id_cliente
        JOIN usuarios ON clientes.id_usuario = usuarios.id_usuario
        WHERE p.id_restaurante = (SELECT id_restaurante FROM restaurantes WHERE id_usuario = %s)
        ORDER BY p.fecha_pedido DESC
        """
        cursor.execute(query, (usuario["id_usuario"],))
        pedidos = cursor.fetchall()

        if not pedidos:
            print("⚠ No tienes pedidos actualmente.")
            return

        print("\n📦 Pedidos recibidos:")
        for p in pedidos:
            print(f"🆔 Pedido {p['id_pedido']} | Cliente: {p['cliente']} ({p['telefono']} - {p['email']})")
            print(f"📍 Dirección de entrega: {p['direccion_entrega']}")
            print(f"💰 Total: ${p['total']} | Estado: {p['estado']} | Fecha: {p['fecha_pedido']}\n")

    except mysql.connector.Error as err:
        print(f"⚠ Error: {err}")

    finally:
        cursor.close()
        conn.close()


#VER PEDIDOS REPARTIDOR

def ver_pedidos_repartidor(usuario):
    """ Muestra los pedidos asignados a un repartidor, incluyendo la dirección de entrega """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        SELECT r.id_reparto, p.id_pedido, res.nombre_comercial AS restaurante, 
               p.total, r.estado, p.direccion_entrega
        FROM reparto_pedidos r
        JOIN pedidos p ON r.id_pedido = p.id_pedido
        JOIN restaurantes res ON p.id_restaurante = res.id_restaurante
        WHERE r.id_repartidor = (SELECT id_repartidor FROM repartidores WHERE id_usuario=%s)
        ORDER BY p.fecha_pedido DESC
        """
        cursor.execute(query, (usuario["id_usuario"],))
        pedidos = cursor.fetchall()

        if not pedidos:
            print("⚠ No tienes pedidos asignados en este momento.")
            return

        print("\n🚚 Pedidos asignados:")
        for p in pedidos:
            print(f"🆔 Pedido {p['id_pedido']} | Restaurante: {p['restaurante']}")
            print(f"📍 Dirección de entrega: {p['direccion_entrega']}")
            print(f"💰 Total: ${p['total']} | Estado: {p['estado']}\n")

    except mysql.connector.Error as err:
        print(f"⚠ Error: {err}")

    finally:
        cursor.close()
        conn.close()


# ASIGNAR PEDIDO A REPARTIDOR

def asignar_pedido_a_repartidor(id_pedido):
    """ Asigna un pedido a un repartidor disponible y actualiza estados """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor()

    # Buscar un repartidor disponible
    cursor.execute("SELECT id_repartidor FROM repartidores WHERE disponible = TRUE ORDER BY RAND() LIMIT 1")
    repartidor = cursor.fetchone()

    if repartidor:
        id_repartidor = repartidor[0]

        try:
            # Asignar el pedido al repartidor
            query = "INSERT INTO reparto_pedidos (id_pedido, id_repartidor, estado) VALUES (%s, %s, 'en camino')"
            cursor.execute(query, (id_pedido, id_repartidor))

            # Marcar al repartidor como "NO DISPONIBLE"
            cursor.execute("UPDATE repartidores SET disponible = FALSE WHERE id_repartidor = %s", (id_repartidor,))

            # Actualizar el estado del pedido a "en camino"
            cursor.execute("UPDATE pedidos SET estado = 'en camino' WHERE id_pedido = %s", (id_pedido,))

            conn.commit()
            print(f"✅ Pedido {id_pedido} asignado al repartidor {id_repartidor}. Estado del pedido: en camino.")

        

        except mysql.connector.Error as err:
            print(f"⚠ Error: {err}")
        
    else:
        print("⚠ No hay repartidores disponibles en este momento.")

    cursor.close()
    conn.close()

#MARCAR PEDIDO ENTREGADO

def marcar_pedido_entregado(usuario, id_pedido):
    """ Permite a un repartidor marcar un pedido como entregado """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor()

    try:
        # Verificar si el pedido está asignado al repartidor
        cursor.execute("SELECT id_reparto FROM reparto_pedidos WHERE id_pedido = %s AND id_repartidor = (SELECT id_repartidor FROM repartidores WHERE id_usuario = %s)", (id_pedido, usuario["id_usuario"]))
        reparto = cursor.fetchone()

        if not reparto:
            print("⚠ No tienes asignado este pedido.")
            return

        # Marcar el pedido como "entregado"
        cursor.execute("UPDATE pedidos SET estado = 'entregado' WHERE id_pedido = %s", (id_pedido,))
        cursor.execute("UPDATE reparto_pedidos SET estado = 'entregado' WHERE id_pedido = %s", (id_pedido,))

        # Marcar al repartidor como "DISPONIBLE"
        cursor.execute("UPDATE repartidores SET disponible = TRUE WHERE id_usuario = %s", (usuario["id_usuario"],))

        conn.commit()
        print(f"✅ Pedido {id_pedido} entregado. Ahora estás DISPONIBLE para recibir nuevos pedidos.")

    except mysql.connector.Error as err:
        print(f"⚠ Error: {err}")

    finally:
        cursor.close()
        conn.close()
# RESEÑAS
def opinar_sobre_pedido(usuario):
    """ Permite al cliente dejar una reseña después de recibir el pedido """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)

    try:
        # Mostrar pedidos entregados sin reseña aún
        query = """
        SELECT p.id_pedido, r.nombre_comercial 
        FROM pedidos p
        JOIN restaurantes r ON p.id_restaurante = r.id_restaurante
        WHERE p.estado = 'entregado' 
        AND p.id_cliente = (SELECT id_cliente FROM clientes WHERE id_usuario=%s)
        AND NOT EXISTS (
            SELECT 1 FROM resenyas 
            WHERE resenyas.id_pedido = p.id_pedido
        )
        """
        cursor.execute(query, (usuario["id_usuario"],))
        pedidos = cursor.fetchall()

        if not pedidos:
            print("⚠ No tienes pedidos entregados pendientes de reseña.")
            return

        print("\n📦 Pedidos para calificar:")
        for p in pedidos:
            print(f"🆔 Pedido {p['id_pedido']} - Restaurante: {p['nombre_comercial']}")

        id_pedido = input("Elige el ID del pedido a calificar: ")
        calificacion = int(input("🔢 Calificación (1-5): "))
        comentario = input("✍️ Comentario: ")

        # Obtener IDs de restaurante y repartidor del pedido
        cursor.execute("""
        SELECT p.id_restaurante, rp.id_repartidor
        FROM pedidos p
        JOIN reparto_pedidos rp ON rp.id_pedido = p.id_pedido
        WHERE p.id_pedido = %s
        """, (id_pedido,))
        info = cursor.fetchone()

        if not info:
            print("❌ No se pudo obtener información del pedido.")
            return

        # Insertar la reseña
        cursor.execute("""
        INSERT INTO resenyas (id_cliente, id_restaurante, id_repartidor, id_pedido, calificación, comentario)
        VALUES ((SELECT id_cliente FROM clientes WHERE id_usuario=%s), %s, %s, %s, %s, %s)
        """, (
            usuario["id_usuario"],
            info["id_restaurante"],
            info["id_repartidor"],
            id_pedido,
            calificacion,
            comentario
        ))

        conn.commit()
        print("✅ ¡Gracias por dejar tu reseña!")

    except mysql.connector.Error as err:
        print(f"⚠ Error: {err}")
    finally:
        cursor.close()
        conn.close()

#VER RESEÑAS RESTAURANTE

def ver_reseñas_restaurante(usuario):
    """ Muestra las reseñas que ha recibido el restaurante logueado """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        SELECT u.nombre AS cliente, r.calificación, r.comentario, r.fecha_reseña
        FROM resenyas r
        JOIN clientes c ON r.id_cliente = c.id_cliente
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        WHERE r.id_restaurante = (SELECT id_restaurante FROM restaurantes WHERE id_usuario = %s)
        ORDER BY r.fecha_reseña DESC
        """
        cursor.execute(query, (usuario["id_usuario"],))
        reseñas = cursor.fetchall()

        if not reseñas:
            print("⚠ No tienes reseñas aún.")
            return

        print("\n🌟 Reseñas de Clientes:")
        for r in reseñas:
            print(f"👤 {r['cliente']} | ⭐ {r['calificación']} | 🗓️ {r['fecha_reseña']}")
            print(f"💬 {r['comentario']}\n")

    except mysql.connector.Error as err:
        print(f"⚠ Error: {err}")
    finally:
        cursor.close()
        conn.close()

def ver_reseñas_de_restaurante(id_restaurante):
    """ Muestra reseñas de un restaurante específico """
    conn = conectar_BBDD()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
        SELECT u.nombre AS cliente, r.calificación, r.comentario, r.fecha_reseña
        FROM resenyas r
        JOIN clientes c ON r.id_cliente = c.id_cliente
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        WHERE r.id_restaurante = %s
        ORDER BY r.fecha_reseña DESC
        """, (id_restaurante,))
        reseñas = cursor.fetchall()

        if not reseñas:
            print("⚠ Este restaurante aún no tiene reseñas.")
            return

        print("\n📝 Reseñas del restaurante:")
        for r in reseñas:
            print(f"👤 {r['cliente']} | ⭐ {r['calificación']} | 🗓️ {r['fecha_reseña']}")
            print(f"💬 {r['comentario']}\n")

    except mysql.connector.Error as err:
        print(f"⚠ Error: {err}")
    finally:
        cursor.close()
        conn.close()