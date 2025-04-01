import mysql
from BBDD import conectar_BBDD
from utils import registrar_usuario, login_usuario, usuario_existe, menu_restaurante, menu_repartidor, menu_cliente, eliminar_usuario

def main():
    while True:
        print("\n🔹 Bienvenido a QueCosaPediste")
        print("1️⃣ Registrarse")
        print("2️⃣ Iniciar sesión")
        print("3️⃣ Eliminar usuario")
        print("4️⃣ Salir")

        opcion = input("Elige una opción (1/2/3/4): ")

        if opcion == "1":
            nombre = input("Nombre: ")
            email = input("Email: ")
            contraseña = input("Contraseña: ")
            telefono = input("Teléfono: ")
            rol = input("Rol (cliente/restaurante/repartidor): ").lower()

            if rol not in ["cliente", "restaurante", "repartidor"]:
                print("❌ Rol no válido. Inténtalo de nuevo.")
                continue
            
            registrar_usuario(nombre, email, contraseña, telefono, rol)

            # Preguntar si quiere iniciar sesión después del registro
            opcion_login = input("\n¿Quieres iniciar sesión ahora? (Sí/No): ").strip().lower()
            if opcion_login in ["sí", "si"]:
                opcion = "2"  # Forzar el inicio de sesión en la siguiente iteración

        if opcion == "2":
            email = input("Email: ")
            contraseña = input("Contraseña: ")
            usuario = login_usuario(email, contraseña)

            if usuario:
                print(f"✅ Bienvenido {usuario['nombre']}, tu rol es {usuario['rol']}.")

                # Redirigir al menú según el rol
                if usuario["rol"] == "restaurante":
                    menu_restaurante(usuario)
                elif usuario["rol"] == "repartidor":
                    menu_repartidor(usuario)
                elif usuario["rol"] == "cliente":
                    menu_cliente(usuario)
            else:
                print("❌ Error al iniciar sesión.")

        elif opcion == "3":
            email = input("Ingrese el email del usuario a eliminar: ")
            eliminar_usuario(email)

        elif opcion == "4":
            print("👋 Saliendo del sistema...")
            break

        else:
            print("⚠ Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()



