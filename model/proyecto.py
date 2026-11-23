from .empleado import Empleado
from config.app_config import conectar_db, oracledb

def validar_tabla_proyectos():
    consulta_sql = """
        create table if not exists proyectos (
            id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre varchar2(100) not null,
            descripcion varchar2(200) not null,
            fecha_inicio date not null,
            id_encargado number not null,
            CONSTRAINT uq_proyecto UNIQUE (nombre, descripcion, fecha_inicio),
            FOREIGN KEY(id_encargado) REFERENCES empleados(id)
        );
    """
    conn = None
    cursor = None

    try:
        print("Intentando validar tabla proyectos...")
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_sql)
            print("[INFO] Tabla proyectos validada correctamente")
    except Exception as e:
        print(f"[ERROR] Validación de tabla proyectos | {e}")
    finally:
        if cursor:
            cursor.close()
            
        if conn:
            conn.close()

def insertar_datos_proyecto(proyecto: Proyecto):
    consulta_select_usuario = """
        select id from usuarios
        where usuarios.correo = :1;
    """

    consulta_select_encargado = """
        select id from empleados
        where empleados.id_usuario = :1;
    """

    consulta_insert = """
        insert into proyectos (
            nombre,
            descripcion,
            fecha_inicio,
            id_encargado
        ) 
        values (:1, :2, :3, :4);
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            cursor.execute(consulta_select_usuario, (proyecto.encargado.correo,))
            id_usuario = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_select_encargado, (id_usuario,))
            id_encargado = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_insert, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, id_encargado))
            conn.commit()

            print("[INFO] Proyecto registrado correctamente")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] Este proyecto ya fue registrado") # ORA-00001: prohibición de datos duplicados
        elif error.code == 942:
            print("[WARNING] Proyecto no se logro registrar | Tabla usuarios no existe") # ORA-00942: intento de acceso a tabla inexistente
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

def validar_tabla_proyectos_por_empleado():
    consulta_sql = """
        create table if not exists proyectos_por_empleado (
            id_empleado number not null,
            id_proyecto number not null,
            PRIMARY KEY(id_empleado, id_proyecto),
            FOREIGN KEY(id_empleado) REFERENCES empleados(id),
            FOREIGN KEY(id_proyecto) REFERENCES proyectos(id)
        );
    """
    conn = None
    cursor = None

    try:
        print("Intentando validar relacion proyectos-empleados...")
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_sql)
            print("[INFO] Tabla de relaciones validada correctamente")
    except Exception as e:
        print(f"[ERROR] Validación de tabla de relaciones | {e}")
    finally:
        if cursor:
            cursor.close()
            
        if conn:
            conn.close()

def insertar_relacion_proyecto_por_empleado(proyecto: Proyecto, empleado: Empleado):
    consulta_select_proyecto = """
            select id from proyectos
            where (
                    proyectos.nombre = :1
                    and proyectos.descripcion = :2
                    and proyectos.fecha_inicio = :3
                );
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
        insert into proyectos_por_empleado (
            id_empleado,
            id_proyecto
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

            cursor.execute(consulta_select_proyecto, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio))
            id_proyecto = str(cursor.fetchall()[0][0])
            
            cursor.execute(consulta_insert, (id_empleado, id_proyecto))
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

def eliminar_relacion_proyecto_por_empleado(proyecto: Proyecto, empleado: Empleado):
    consulta_select_proyecto = """
            select id from proyectos
            where (
                    proyectos.nombre = :1
                    and proyectos.descripcion = :2
                    and proyectos.fecha_inicio = :3
                );
        """
    
    consulta_select_usuario = """
            select id from usuarios
            where usuarios.correo = :1;
        """

    consulta_select_empleado = """
            select id from empleados
            where empleados.id_usuario = :1;
        """
    
    consulta_delete = """
            delete from proyectos_por_empleado
            where (id_empleado = :1 and id_proyecto = :2)
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

            cursor.execute(consulta_select_proyecto, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio))
            id_proyecto = str(cursor.fetchall()[0][0])
            
            cursor.execute(consulta_delete, (id_empleado, id_proyecto))
            conn.commit()

            print("[INFO] Relacion eliminada correctamente")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 942:
            print("[WARNING] Relacion no se logro identificar | Una o más de las tablas independientes no existe") # ORA-00942: intento de acceso a tabla inexistente
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

class Proyecto():
    def __init__(self, nombre: str, descripcion: str, fecha_inicio: str, encargado: Empleado):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.encargado = encargado

        validar_tabla_proyectos()
        insertar_datos_proyecto(self)

    def asignar_empleado(self, empleado: Empleado):
        validar_tabla_proyectos_por_empleado()
        insertar_relacion_proyecto_por_empleado(self, empleado)
        print(f"Empleado {empleado.nombre} asignado a proyecto {self.nombre}.")

    def deasignar_empleado(self, empleado: Empleado):
        validar_tabla_proyectos_por_empleado()
        eliminar_relacion_proyecto_por_empleado(self, empleado)