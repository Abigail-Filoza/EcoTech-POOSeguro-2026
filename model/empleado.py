from .usuario import Usuario, conectar_db, oracledb
from .registrohorario import RegistroHorario

def validar_tabla_empleados():
    consulta_sql = """
        create table if not exists empleados (
            id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            id_usuario number unique,
            direccion varchar2(75) not null,
            telefono varchar2(25) not null,
            fecha_inicio_contrato date not null,
            salario number not null,
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
        );
    """
    conn = None
    cursor = None

    try:
        print("Intentando validar tabla empleados...")
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_sql)
            print("[INFO] Tabla empleados validada correctamente")
    except Exception as e:
        print(f"[ERROR] Validación de tabla empleados | {e}")
    finally:
        if cursor:
            cursor.close()
            
        if conn:
            conn.close()

def insertar_datos_empleado(empleado: Empleado):
    consulta_select_usuario = """
        select id from usuarios
        where usuarios.correo = :1;
    """

    consulta_insert = """
        insert into empleados (
            id_usuario,
            direccion,
            telefono,
            fecha_inicio_contrato,
            salario
        ) 
        values (:1, :2, :3, :4, :5);
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            cursor.execute(consulta_select_usuario, (empleado.correo,))
            id_usuario = str(cursor.fetchall()[0][0])

            cursor.execute(consulta_insert, (id_usuario, empleado.direccion, empleado.telefono, empleado.fecha_inicio_contrato, empleado.salario))
            conn.commit()

            print("[INFO] Empleado registrado correctamente")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] Este empleado ya fue registrado") # ORA-00001: prohibición de datos duplicados
        elif error.code == 942:
            print("[WARNING] Empleado no se logro registrar | Tabla usuarios no existe") # ORA-00942: intento de acceso a tabla inexistente
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Empleado no se logro registrar | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

class Empleado(Usuario):
    def __init__(self, nombre: str, correo: str, clave: str, direccion: str, telefono: int, fecha_inicio_contrato: str, salario: int):
        super().__init__(nombre, correo, clave)
        self.direccion = direccion
        self.telefono = telefono
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario

        validar_tabla_empleados()
        insertar_datos_empleado(self)

    def registrar_horas(self, p_fecha: str, p_horas_trabajadas: float, p_desc_tareas: str):
        nuevo_registro = RegistroHorario(self,
                                         p_fecha,
                                         p_horas_trabajadas,
                                         p_desc_tareas) #Al integrar BBDD esto se cambiara
                                                        #Para usar de forma automatica el
                                                        #proyecto al que este asignado el empleado

        #return tambien sujeto a cambio (placeholder)
        return f"{p_horas_trabajadas}hrs registradas a nombre de {self.nombre}"