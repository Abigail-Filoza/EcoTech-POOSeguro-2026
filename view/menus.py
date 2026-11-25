from getpass import getpass
from model.usuario import Usuario, iniciar_sesion
from model.adminrrhh import AdminRRHH
from model.administradorsistema import AdministradorDeSistema, ROLES_VALIDOS

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

def pedir_entero(texto: str):
    try:
        return int(input(texto))
    except ValueError:
        print(" Debe ingresar un número entero.")
        return None

def elegir_departamento(admin: AdminRRHH):
    departamentos = admin.listar_departamentos()

    if not departamentos:
        print(" No hay departamentos registrados.")
        return None

    for d in departamentos:
        print(f"  {d.id_departamento} : {d.nombre} (gerente: {d.id_gerente})")

    id_elegido = pedir_entero(" Id del departamento : ")

    return next((d for d in departamentos if d.id_departamento == id_elegido), None)

def menu_departamentos(admin: AdminRRHH):
    opcion = input("\n 1 : Listar\n 2 : Crear\n 3 : Editar\n 4 : Eliminar\n 5 : Volver\n\n Opción : ")

    try:
        if opcion == "1":
            for d in admin.listar_departamentos():
                print(f"  {d.id_departamento} : {d.nombre} (gerente: {d.id_gerente})")
        elif opcion == "2":
            nombre = input(" Nombre : ")
            id_gerente = pedir_entero(" Id del gerente : ")

            if id_gerente is not None:
                admin.crear_departamento(nombre, id_gerente)
        elif opcion in ("3", "4"):
            departamento = elegir_departamento(admin)

            if departamento is None:
                print(" Departamento no encontrado.")
            elif opcion == "3":
                nombre = input(" Nuevo nombre : ")
                id_gerente = pedir_entero(" Nuevo id del gerente : ")

                if id_gerente is not None:
                    admin.editar_departamento(departamento, nombre, id_gerente)
            else:
                admin.eliminar_departamento(departamento)
        elif opcion != "5":
            print(" Opción no válida, intente nuevamente.")
    except ValueError as e:  # validaciones de Departamento
        print(f" {e}")

def menu_roles(admin: AdministradorDeSistema):
    opcion = input("\n 1 : Agregar rol\n 2 : Quitar rol\n 3 : Volver\n\n Opción : ")

    if opcion in ("1", "2"):
        correo = input(" Correo del usuario : ").strip()
        print(f" Roles disponibles: {', '.join(ROLES_VALIDOS)}")
        rol = input(" Rol : ").strip()

        if opcion == "1":
            admin.agregar_rol(correo, rol)
        else:
            admin.quitar_rol(correo, rol)
    elif opcion != "3":
        print(" Opción no válida, intente nuevamente.")

def menu_usuario(usuario):
    """Se ejecuta mientras haya sesión iniciada; devuelve el usuario o None al cerrar."""
    print(f"\n Bienvenido, {usuario.nombre}")

    texto = "\n 1 : Cambiar contraseña"

    if usuario.tiene_rol("admin_rrhh"):
        texto += "\n 2 : Gestionar departamentos"
    if usuario.tiene_rol("admin_sistema"):
        texto += "\n 3 : Gestionar roles"

    opcion = str(input(texto + "\n 0 : Cerrar sesión\n\n Opción : "))

    if opcion == "0":
        usuario.cerrar_sesion()
        return None
    elif opcion == "1":
        usuario.cambiar_contrasena(getpass(" Nueva contraseña : "))
    elif opcion == "2" and usuario.tiene_rol("admin_rrhh"):
        menu_departamentos(AdminRRHH(usuario))
    elif opcion == "3" and usuario.tiene_rol("admin_sistema"):
        menu_roles(AdministradorDeSistema(usuario))
    else:
        print(" Opción no válida, intente nuevamente.")

    return usuario