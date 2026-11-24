from getpass import getpass
from model.usuario import Usuario, iniciar_sesion 

def pedir_login(max_intentos: int = 3):
    for intento in range(1, max_intentos + 1):
        correo = input(" Correo     : ").strip()
        clave = getpass(" Contraseña : ")
        usuario = iniciar_sesion(correo, clave)

        if usuario:
            return usuario

        print(f" Intento {intento} de {max_intentos}")

    print(" Demasiados intentos fallidos.")
    return False

def menu_principal(usuario):
    """Devuelve (usuario, programa_activo)."""
    print("=====" * 6)
    print("\n Seleccione una opción:")

    opcion = str(input(
        "\n 1 : Iniciar sesión" +
        "\n 2 : Terminar programa" +
        "\n 3 : Registrar usuario" +
        "\n\n Opción : "
    ))

    if opcion == "1":
        usuario = pedir_login()
    elif opcion == "2":
        print(" Que le vaya bien.")
        return usuario, False
    elif opcion == "3":
        nombre = input(" Nombre     : ").strip()
        correo = input(" Correo     : ").strip()
        clave = getpass(" Contraseña : ")

        if nombre and correo and clave:
            Usuario(nombre, correo, clave)  # el constructor crea la tabla e inserta
        else:
            print(" Todos los campos son obligatorios.")
    else:
        print(" Opción no válida, intente nuevamente.")

    return usuario, True

def menu_usuario(usuario):
    """Se ejecuta mientras haya sesión iniciada; devuelve el usuario o None al cerrar."""
    print(f"\n Bienvenido, {usuario.nombre}")

    opcion = str(input(
        "\n 1 : Cambiar contraseña" +
        "\n 2 : Cerrar sesión" +
        "\n\n Opción : "
    ))

    if opcion == "1":
        usuario.cambiar_contrasena(getpass(" Nueva contraseña : "))
    elif opcion == "2":
        usuario.cerrar_sesion()
        return None
    else:
        print(" Opción no válida, intente nuevamente.")

    return usuario