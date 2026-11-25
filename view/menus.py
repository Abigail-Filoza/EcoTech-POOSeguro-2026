from getpass import getpass
from model.usuario import Usuario
from model.empleado import Empleado
from model.adminrrhh import AdminRRHH
from utils.metodos import pedir_entero
from utils.metodos_bd import consultar_id_empleado, consultar

def pedir_login(max_intentos: int = 3):
    for intento in range(1, max_intentos + 1):
        usuario_aux = Usuario("test","test","test",[],False)

        correo = input(" Correo     : ").strip()
        clave = getpass(" Contraseña : ")
        usuario = usuario_aux.iniciar_sesion(correo, clave)

        if usuario:
            return usuario

        print(f" Intento {intento} de {max_intentos}")

    print(" Demasiados intentos fallidos.")
    return False

def menu_inicial(usuario: Usuario):
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

def menu_usuario(usuario: Usuario):
    print(f"\n Bienvenido, {usuario.nombre}")

    es_rrhh = usuario.tiene_rol("admin_rrhh") or usuario.tiene_rol("admin_sistema")
    texto = "\n 1 : Cambiar contraseña"

    if es_rrhh:
        texto += "\n 2 : Gestionar departamentos\n 3 : Registrar empleado"

    opcion = str(input(texto + "\n 0 : Cerrar sesión\n\n Opción : "))

    if opcion == "0":
        usuario.cerrar_sesion()
        return None
    elif opcion == "1":
        usuario.cambiar_contrasena(getpass(" Nueva contraseña : "))
    elif opcion == "2" and es_rrhh:
        menu_departamentos(AdminRRHH(usuario))
    elif opcion == "3" and es_rrhh:
        menu_registrar_empleado(AdminRRHH(usuario))
    else:
        print(" Opción no válida, intente nuevamente.")

    return usuario

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
            nombre = input(" Nombre del departamento : ")
            gerente, valido = pedir_gerente()

            if valido:
                admin.crear_departamento(nombre, gerente)
        elif opcion in ("3", "4"):
            departamento = elegir_departamento(admin)

            if departamento is None:
                print(" Departamento no encontrado.")
            elif opcion == "3":
                nombre = input(" Nuevo nombre del departamento : ")
                gerente, valido = pedir_gerente()

                if valido:
                    admin.editar_departamento(departamento, nombre, gerente)
            else:
                admin.eliminar_departamento(departamento)
        elif opcion != "5":
            print(" Opción no válida, intente nuevamente.")
    except ValueError as e:  # validaciones de Departamento
        print(f"[ERROR] {e}")

def pedir_gerente():
    correo = input(" Correo del gerente : ").strip()

    if not correo:
        return None, False

    id_gerente = consultar_id_empleado(correo)

    datos_usuario_gerente = consultar("select * from usuarios where correo= :1",(correo,))
    datos_empleado_gerente = consultar("select * from empleados where id= :1",(id_gerente,))
    gerente = Empleado(datos_usuario_gerente[0][1],
                       datos_usuario_gerente[0][2],
                       datos_usuario_gerente[0][3],
                       datos_empleado_gerente[0][1],
                       datos_empleado_gerente[0][2],
                       datos_empleado_gerente[0][3],
                       datos_empleado_gerente[0][4],
                       False)

    if gerente is None:
        print(" Usuario no encontrado.")
        return None, False

    return gerente, True

def menu_registrar_empleado(admin: AdminRRHH):
    nombre = input(" Nombre : ").strip()
    correo = input(" Correo : ").strip()
    clave = getpass(" Clave inicial : ")
    direccion = input(" Dirección : ").strip()
    telefono = input(" Teléfono : ").strip()
    fecha = input(" Fecha inicio contrato (YYYY-MM-DD) : ").strip()
    salario = pedir_entero(" Salario : ")
    departamento = elegir_departamento(admin)

    if not all([nombre, correo, clave, direccion, telefono, fecha]) or salario is None or departamento is None:
        print(" Datos incompletos, no se registró el empleado.")
        return

    print(" " + admin.registrar_empleado(nombre, correo, clave, direccion, telefono, fecha,
                                         salario, departamento.id_departamento))
