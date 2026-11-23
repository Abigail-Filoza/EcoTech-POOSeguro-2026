from utils.metodos_bd import ejecutar_consulta
from config.app_config import conectar_db, oracledb
from .proyecto import Proyecto
from .empleado import Empleado

def validar_datos_departamento(nombre, gerente):
    if not isinstance(nombre, str) or not nombre.strip():
        print("El nombre del departamento es obligatorio y debe ser de tipo String")
        return False
    elif len(nombre.strip()) > 100:
        print("El nombre no puede superar los 100 caracteres")
        return False
    elif not isinstance(gerente, Empleado):
        print("El cargo gerente debe corresponder a un empleado existente")
        return False
    else:
        return True

def validar_tabla_departamentos():
    consulta_sql = """
        create table if not exists departamentos (
            id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre varchar2(100) not null unique,
            id_gerente number not null,
            FOREIGN KEY(id_gerente) REFERENCES empleados(id)
        );
    """

    errores = {1: "Ya existe un departamento con ese nombre"}

    ejecutar_consulta(consulta_sql,
                      None,
                      "Tabla departamentos validada correctamente",
                      "Validación de tabla departamentos abortada",
                      errores)

def insertar_datos_departamento(depto: Departamento):
    consulta_select_usuario = """
        select id from usuarios
        where usuarios.correo = :1;
    """

    consulta_select_gerente = """
        select id from empleados
        where empleados.id_usuario = :1;
    """

    consulta_insert = """
        insert into departamentos (
            nombre,
            id_gerente
        ) 
        values (:1, :2);
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            cursor.execute(consulta_select_usuario, (depto.gerente.correo,))
            id_usuario = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_select_gerente, (id_usuario,))
            id_gerente = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_insert, (depto.nombre, id_gerente))
            conn.commit()

            print("[INFO] Departamento registrado correctamente")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] Este departamento ya fue registrado") # ORA-00001: prohibición de datos duplicados
        elif error.code == 942:
            print("[WARNING] Departamento no se logro registrar | Tabla usuarios no existe") # ORA-00942: intento de acceso a tabla inexistente
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Departamento no se logro registrar | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def update_datos_bd(depto: Departamento, nombre_ref: str):
    consulta_select_usuario = """
        select id from usuarios
        where usuarios.correo = :1;
    """

    consulta_select_gerente = """
        select id from empleados
        where empleados.id_usuario = :1;
    """

    consulta_update = """
        update departamentos
        set nombre = :2, id_gerente = :3
        where nombre = :1;
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            cursor.execute(consulta_select_usuario, (depto.gerente.correo,))
            id_usuario = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_select_gerente, (id_usuario,))
            id_gerente = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_update, (nombre_ref, depto.nombre, id_gerente))
            conn.commit()

            print("[INFO] Proyecto registrado correctamente")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] Este departamento ya fue registrado") # ORA-00001: prohibición de datos duplicados
        elif error.code == 942:
            print("[WARNING] Departamento no se logro registrar | Tabla usuarios no existe") # ORA-00942: intento de acceso a tabla inexistente
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Departamento no se logro registrar | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def actualizar_proyecto_bd(proyecto: Proyecto, nombre_ref, encargado_ref, desc_ref):
    consulta_proyecto = """
                    select id from proyectos
                    where (nombre = :1
                            and descripcion = :2
                            and fecha_inicio = :3;
                    """

    consulta_usuario = """
                    select id from usuarios
                    where id = :1;
                    """

    consulta_encargado = """
                    select id from empleados
                    where id_usuario = :1;
                    """
    
    consulta_update = """
                    update proyectos set (nombre = :1, descripcion = :2, id_encargado = :3)
                    where id = :4;
                    """

    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            cursor.execute(consulta_usuario, (encargado_ref.correo,))
            id_usuario = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_encargado, (id_usuario,))
            id_encargado = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_proyecto, (nombre_ref, desc_ref, proyecto.fecha_inicio))
            id_proyecto = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_update, (proyecto.nombre,
                                             proyecto.descripcion,
                                             id_encargado,
                                             id_proyecto))
            conn.commit()

            print("[INFO] Proyecto actualizado correctamente")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] Proyecto con este nombre ya existe") # ORA-00001: prohibición de datos duplicados
        elif error.code == 942:
            print("[WARNING] Proyecto no se logro actualizar | Tabla usuarios no existe") # ORA-00942: intento de acceso a tabla inexistente
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Proyecto no se logro registrar | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def validar_tabla_empleados_por_depto():
    consulta_sql = """
        create table if not exists empleados_por_departamento (
            id_empleado number not null unique,
            id_departamento number not null,
            FOREIGN KEY(id_empleado) REFERENCES empleados(id),
            FOREIGN KEY(id_departamento) REFERENCES departamentos(id)
        );
    """

    ejecutar_consulta(consulta_sql,
                      None,
                      "Tabla departamentos validada correctamente",
                      "Validación de tabla departamentos abortada")

def insertar_relacion_empleado_por_depto(depto: Proyecto, empleado: Empleado):
    consulta_select_depto = """
            select id from departamentos
            where nombre = :1;
        """
    
    consulta_select_usuario = """
            select id from usuarios
            where usuarios.correo = :1;
        """

    consulta_select_empleado = """
            select id from empleados
            where empleados.id_usuario = :1;
        """

    consulta_insert = """
        insert into empleados_por_depto (
            id_empleado,
            id_departamento
        ) 
        values (:1, :2);
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            cursor.execute(consulta_select_usuario, (empleado.correo,))
            id_usuario = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_select_empleado, (id_usuario,))
            id_empleado = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_select_depto, (depto.nombre,))
            id_depto = str(cursor.fetchall()[0][0])
            
            cursor.execute(consulta_insert, (id_empleado, id_depto))
            conn.commit()

            print("[INFO] Relacion registrada correctamente")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] Esta relacion ya fue registrada") # ORA-00001: prohibición de datos duplicados
        elif error.code == 942:
            print("[WARNING] Relacion no se logro registrar | Una o más de las tablas independientes no existe") # ORA-00942: intento de acceso a tabla inexistente
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Relacion no se logro registrar | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def eliminar_relacion_empleado_por_depto(empleado: Empleado):
    consulta_select_usuario = """
            select id from usuarios
            where usuarios.correo = :1;
        """

    consulta_select_empleado = """
            select id from empleados
            where empleados.id_usuario = :1;
        """
    
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            cursor.execute(consulta_select_usuario, (empleado.correo,))
            id_usuario = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_select_empleado, (id_usuario,))
            id_empleado = str(cursor.fetchall()[0][0])

            cursor.execute("delete from empleados_por_departamento where id_empleado = :1",
                           (id_empleado,))
            conn.commit()

            print("[INFO] Relacion eliminada correctamente")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 942:
            print("[WARNING] Relacion no se logro eliminar | Tabla usuarios no existe") # ORA-00942: intento de acceso a tabla inexistente
        elif error.code == 2292:
            print("[WARNING] Relacion no se logro eliminar | Tiene registros asociados")
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Relacion no se logro eliminar | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()
    
class Departamento():
    def __init__(self, nombre: str, gerente: Empleado):
        if validar_datos_departamento(nombre, gerente):
            self.nombre = nombre
            self.gerente = gerente

            validar_tabla_departamentos()
            insertar_datos_departamento(self)

    def crear_proyecto(self, p_nombre: str, p_descripcion: str, p_fecha_inicio: str, p_encargado: Empleado):
        nuevo_proyecto = Proyecto(p_nombre, p_descripcion, p_fecha_inicio, p_encargado)

    def editar_proyecto(self, proyecto: Proyecto, p_nombre: str, p_descripcion: str, p_encargado: Empleado):
        nombre_ref = proyecto.nombre
        encargado_ref = proyecto.encargado
        desc_ref = proyecto.descripcion

        proyecto.nombre = p_nombre
        proyecto.descripcion = p_descripcion
        proyecto.encargado = p_encargado

        actualizar_proyecto_bd(proyecto, nombre_ref, encargado_ref, desc_ref)  

    def eliminar_proyecto(self, proyecto: Proyecto):
        errores = {2292: "No se puede eliminar: tiene registros asociados"}

        ejecutar_consulta(
            "delete from proyectos where nombre = :1",
            (proyecto.nombre),
            "Proyecto eliminado correctamente",
            "Proyecto no se pudo eliminar",
            "El proyecto no existe",
            errores)

    def asignar_empleado(self, empleado: Empleado):
        insertar_relacion_empleado_por_depto(self, empleado)

    def reasignar_empleado(self, empleado: Empleado, departamento_destino: "Departamento"):
        if not isinstance(empleado, Empleado):
            print("Empleado inválido | No corresponde a tipo Empleado")
            return

        if not isinstance(departamento_destino, Departamento) or departamento_destino.id_departamento is None:
            print("Departamento destino inválido | No está registrado en la base de datos")
            return

        eliminar_relacion_empleado_por_depto(empleado)
        insertar_relacion_empleado_por_depto(departamento_destino, empleado)