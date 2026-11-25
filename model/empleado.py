from .usuario import Usuario
from config.app_config import conectar_db, oracledb

def validar_tabla_empleados():
    consulta_sql = """
        create table if not exists empleados (
            id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            id_usuario number not null unique,
            id_departamento number,
            id_proyecto number,
            direccion varchar2(75) not null,
            telefono varchar2(25) not null,
            fecha_inicio_contrato date not null,
            salario number not null,
            constraint fk_empleado_proyecto foreign key (id_proyecto) references proyectos(id),
            constraint fk_empleado_usuario foreign key (id_usuario) references usuarios(id),
            constraint fk_empleado_departamento foreign key (id_departamento)
                references departamentos(id_departamento)
        )
    """
    conn = None
    cursor = None

    try:
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

def insertar_datos_empleado(empleado: "Empleado") -> bool:
    consulta_select_usuario = "select id from usuarios where correo = :1"
    consulta_insert = """
        insert into empleados (id_usuario, id_departamento, direccion, telefono,
                               fecha_inicio_contrato, salario)
        values (:1, :2, :3, :4, to_date(:5, 'YYYY-MM-DD'), :6)
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_select_usuario, (empleado.correo,))
            fila = cursor.fetchone()

            if fila is None:
                print("[WARNING] Empleado no registrado | El usuario no existe")
                return False

            cursor.execute(consulta_insert, (fila[0], empleado.id_departamento, empleado.direccion,
                                             str(empleado.telefono), empleado.fecha_inicio_contrato,
                                             empleado.salario))
            conn.commit()

            print("[INFO] Empleado registrado correctamente")
            return True
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] Este empleado ya fue registrado")        # ORA-00001
        elif error.code == 2291:
            print("[WARNING] El departamento indicado no existe")     # ORA-02291
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

    return False

class Empleado(Usuario):
    def __init__(self, nombre: str, correo: str, clave: str, direccion: str, telefono: int,
                 fecha_inicio_contrato: str, salario: int, id_departamento: int = None):
        super().__init__(nombre, correo, clave)  # crea el usuario (si el correo ya existe, solo avisa)
        self.direccion = direccion
        self.telefono = telefono
        self.fecha_inicio_contrato = fecha_inicio_contrato  # formato YYYY-MM-DD
        self.salario = salario
        self.id_departamento = id_departamento

        self.registrado = insertar_datos_empleado(self)

    # registrar_horas queda exactamente como lo tienes