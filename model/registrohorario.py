from .empleado import Empleado
from .proyecto import Proyecto
from config.app_config import conectar_db, oracledb

def validar_tabla_registros():
    consulta_sql = """
        create table if not exists registros (
            id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            id_empleado number not null,
            fecha date not null,
            horas_trabajadas number not null,
            descripcion_tareas varchar(200),
            id_proyecto number not null,
            CONSTRAINT uq_registro UNIQUE (id_empleado, fecha),
            FOREIGN KEY(id_empleado) REFERENCES empleados(id),
            FOREIGN KEY(id_proyecto) REFERENCES proyectos(id)
        );
    """
    conn = None
    cursor = None

    try:
        print("Intentando validar tabla registros...")
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_sql)
            print("[INFO] Tabla registros validada correctamente")
    except Exception as e:
        print(f"[ERROR] Validación de tabla registros | {e}")
    finally:
        if cursor:
            cursor.close()
            
        if conn:
            conn.close()

def insertar_datos_registro(registro: RegistroHorario):
    consulta_select_usuario = """
        select id from usuarios
        where usuarios.correo = :1;
    """

    consulta_select_empleado = """
        select id from empleados
        where empleados.id_usuario = :1;
    """

    consulta_select_proyecto = """
        select id from proyectos
        where (
            proyectos.nombre = :1
            and proyectos.descripcion = :2
            and proyectos.fecha_inicio = :3
        );
    """

    consulta_insert = """
        insert into registros (
            id_empleado,
            fecha,
            horas_trabajadas,
            descripcion_tareas,
            id_proyecto
        ) 
        values (:1, :2, :3, :4, :5);
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            cursor.execute(consulta_select_usuario, (registro.empleado.correo,))
            id_usuario = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_select_empleado, (id_usuario,))
            id_empleado = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_select_proyecto,(registro.proyecto.nombre, registro.proyecto.descripcion, registro.proyecto.fecha_inicio))
            id_proyecto = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_insert, (id_empleado, registro.fecha, registro.horas_trabajadas, registro.desc_tareas, id_proyecto))
            conn.commit()

            print("[INFO] Registro enviado correctamente")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback() # Si algo falla, nos aseguramos de que nada cambie en la bd

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] Ya existe un registro para el dia ingresado") # ORA-00001: prohibición de datos duplicados
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Registro no se logro enviar | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

class RegistroHorario():
    def __init__(self, empleado: Empleado, fecha: str, horas_trabajadas: float, desc_tareas: str, proyecto: Proyecto):
        self.empleado = empleado
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.desc_tareas = desc_tareas
        self.proyecto = proyecto

        validar_tabla_registros()
        insertar_datos_registro(self)