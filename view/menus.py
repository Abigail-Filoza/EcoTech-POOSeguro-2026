from getpass import getpass
from model.usuario import Usuario, iniciar_sesion
from model.adminrrhh import AdminRRHH
from model.usuario import Usuario, iniciar_sesion, bd_buscar_id_usuario
from model.departamento import Departamento 
from model.proyecto import Proyecto 


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

def pedir_usuario(texto: str):
    """Devuelve (id_usuario, valido). Vacío = sin usuario."""
    correo = input(texto).strip()

    if not correo:
        return None, True

    id_usuario = bd_buscar_id_usuario(correo)

    if id_usuario is None:
        print(" Usuario no encontrado.")
        return None, False

    return id_usuario, True

def elegir_departamento_de(departamentos: list):
    if not departamentos:
        print(" No hay departamentos disponibles.")
        return None

    if len(departamentos) == 1:
        return departamentos[0]

    for d in departamentos:
        print(f"  {d.id_departamento} : {d.nombre}")

    id_elegido = pedir_entero(" Id del departamento : ")

    return next((d for d in departamentos if d.id_departamento == id_elegido), None)

def elegir_proyecto(proyectos: list):
    if not proyectos:
        print(" No hay proyectos disponibles.")
        return None

    for p in proyectos:
        print(f"  {p.id} : {p.nombre} (inicio: {p.fecha_inicio}, encargado: {p.id_encargado})")

    id_elegido = pedir_entero(" Id del proyecto : ")

    return next((p for p in proyectos if p.id == id_elegido), None)

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
            id_gerente, valido = pedir_gerente()

            if valido:
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

def menu_usuario(usuario):
    print(f"\n Bienvenido, {usuario.nombre}")

    

    es_rrhh = usuario.tiene_rol("admin_rrhh") or usuario.tiene_rol("admin_sistema")
    es_gerente = usuario.tiene_rol("gerente")
    es_encargado = usuario.tiene_rol("encargado")
    texto = "\n 1 : Cambiar contraseña"

    if es_rrhh:
        texto += "\n 2 : Gestionar departamentos\n 3 : Registrar empleado"

    opcion = str(input(texto + "\n 0 : Cerrar sesión\n\n Opción : "))

    if opcion == "0":
        usuario.cerrar_sesion()
    if es_gerente:
        texto += "\n 4 : Gestionar proyectos de mi departamento"
    if es_encargado:
        texto += "\n 5 : Gestionar empleados de mi proyecto"
        return None
    elif opcion == "1":
        usuario.cambiar_contrasena(getpass(" Nueva contraseña : "))
    elif opcion == "2" and es_rrhh:
        menu_departamentos(AdminRRHH(usuario))
    elif opcion == "3" and es_rrhh:
        menu_registrar_empleado(AdminRRHH(usuario))
    elif opcion == "4" and es_gerente:
        menu_gerente(usuario)
    elif opcion == "5" and es_encargado:
        menu_encargado(usuario)
    else:
        print(" Opción no válida, intente nuevamente.")

    return usuario
    
def pedir_gerente():
    """Devuelve (id_gerente, valido). Vacío = departamento sin gerente."""
    correo = input(" Correo del gerente (vacío = sin gerente) : ").strip()

    if not correo:
        return None, True

    id_gerente = bd_buscar_id_usuario(correo)

    if id_gerente is None:
        print(" Usuario no encontrado.")
        return None, False

    return id_gerente, True

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
    
def menu_gerente(usuario):
    departamento = elegir_departamento_de(Departamento.listar_por_gerente(usuario.id))

    if departamento is None:
        return

    print(f"\n Departamento: {departamento.nombre}")
    opcion = input("\n 1 : Listar proyectos\n 2 : Crear proyecto\n 3 : Editar proyecto"
                   "\n 4 : Eliminar proyecto\n 5 : Asignar empleado\n 6 : Reasignar empleado"
                   "\n 7 : Volver\n\n Opción : ")

    try:
        if opcion == "1":
            for p in departamento.listar_proyectos():
                print(f"  {p.id} : {p.nombre} (inicio: {p.fecha_inicio}, encargado: {p.id_encargado})")
        elif opcion == "2":
            nombre = input(" Nombre : ")
            descripcion = input(" Descripción : ")
            fecha = input(" Fecha inicio (YYYY-MM-DD) : ").strip()
            id_encargado, valido = pedir_usuario(" Correo del encargado (vacío = sin encargado) : ")

            if valido:
                departamento.crear_proyecto(nombre, descripcion, fecha, id_encargado)
        elif opcion in ("3", "4"):
            proyecto = elegir_proyecto(departamento.listar_proyectos())

            if proyecto is None:
                print(" Proyecto no encontrado.")
            elif opcion == "3":
                nombre = input(" Nuevo nombre : ")
                descripcion = input(" Nueva descripción : ")
                fecha = input(" Nueva fecha inicio (YYYY-MM-DD) : ").strip()
                id_encargado, valido = pedir_usuario(" Correo del encargado (vacío = sin encargado) : ")

                if valido:
                    departamento.editar_proyecto(proyecto.id, nombre, descripcion, fecha, id_encargado)
            else:
                departamento.eliminar_proyecto(proyecto.id)
        elif opcion == "5":
            departamento.asignar_empleado(input(" Correo del empleado : ").strip())
        elif opcion == "6":
            correo = input(" Correo del empleado : ").strip()
            destino = elegir_departamento_de(Departamento.listar())

            if destino is None:
                print(" Departamento destino no encontrado.")
            else:
                departamento.reasignar_empleado(correo, destino)
        elif opcion != "7":
            print(" Opción no válida, intente nuevamente.")
    except ValueError as e:  # validaciones de Proyecto
        print(f" {e}")
        
def menu_encargado(usuario):
    proyecto = elegir_proyecto(Proyecto.listar_por_encargado(usuario.id))

    if proyecto is None:
        return

    print(f"\n Proyecto: {proyecto.nombre}")
    opcion = input("\n 1 : Ver empleados\n 2 : Asignar empleado\n 3 : Desasignar empleado"
                   "\n 4 : Volver\n\n Opción : ")

    if opcion == "1":
        empleados = proyecto.listar_empleados()

        if not empleados:
            print(" El proyecto no tiene empleados asignados.")

        for correo, nombre in empleados:
            print(f"  {nombre} ({correo})")
    elif opcion == "2":
        proyecto.asignar_empleado(input(" Correo del empleado : ").strip())
    elif opcion == "3":
        proyecto.desasignar_empleado(input(" Correo del empleado : ").strip())
    elif opcion != "4":
        print(" Opción no válida, intente nuevamente.")
        
