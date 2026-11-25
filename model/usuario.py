import os
from utils.metodos import bcrypt, hashear_clave
from utils.metodos_bd import consultar
from config.app_config import conectar_db, oracledb

def validar_tabla_usuarios():
    consulta_sql = """
        create table if not exists usuarios (
            id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre varchar2(100) not null,
            correo varchar2(100) not null unique,
            clave varchar2(150) not null
        );
    """
    conn = None
    cursor = None

    try:
        print("Intentando validar tabla usuarios...")
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_sql)
            print("[INFO] Tabla usuarios validada correctamente")
    except Exception as e:
        print(f"[ERROR] Validación de tabla usuarios abortada | {e}")
    finally:
        if cursor:
            cursor.close()
            
        if conn:
            conn.close()

def insertar_datos_usuario(usuario: Usuario):
    consulta_insert = """
        insert into usuarios (nombre, correo, clave)
        values (:1, :2, :3)
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_insert, (usuario.nombre, usuario.correo, usuario.clave))
            conn.commit()

            print("[INFO] Usuario insertado correctamente")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] Este correo ya está en uso") # ORA-00001: prohibición de datos duplicados
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback() # Si algo falla, nos aseguramos de que nada cambie en la bd

        print(f"[ERROR] Usuario no registrado | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def iniciar_sesion_bd(correo: str, clave: str):
    consulta = "select nombre, clave from usuarios where correo = :1"
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta, (correo,))
            datos_usuario = cursor.fetchone()  # (nombre, clave, rol) o None

            if datos_usuario:
                nombre, clave_bd = datos_usuario

                # Se deben transformar ambas claves a bytes para validarlas
                if bcrypt.checkpw(clave.encode('utf-8'), str(clave_bd).encode('utf-8')):
                    print("[INFO] Ingreso correcto")
                    usuario = Usuario(nombre, correo, clave_bd, [], registrar=False)
                    usuario.sesion_activa = True
                    return usuario

            print("[ERROR] Credenciales incorrectas")
            return False
        else:
            print("[ERROR] No se pudo conectar la bd")
            return False
    except Exception as e:
        error = e.args[0]

        if error.code == 942:
            print("[ERROR] Obtención de clave | Tabla usuarios no existe")
        else:
            print(f"[ERROR] Obtención de clave | {e}")
        return False
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def bd_actualizar_clave(usuario: "Usuario", nueva_clave: str):
    consulta_update = """
        update usuarios set clave = :1
        where correo = :2
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_update, (hashear_clave(nueva_clave), usuario.correo))

            if cursor.rowcount == 0:
                print("[WARNING] El usuario no existe en la base de datos")
                return False

            conn.commit()
            print("[INFO] Clave actualizada correctamente")
            return True
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback() # Si algo falla, nos aseguramos de que nada cambie en la bd

        print(f"[ERROR] Clave no se pudo actualizar | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return False

def bd_calcular_roles(id_empleado: int, correo: str) -> set:
    """Los roles no se guardan: se deducen de los datos del sistema."""
    roles = set()

    if correo.lower() == os.getenv("ADMIN_SISTEMA_CORREO", "").lower():
        roles.add("admin_sistema")

    filas = consultar("""
        select
            (select * from departamentos where id_gerente = :1),
            (select * from empleados e
                join proyectos_por_empleado pxe on pxe.id_empleado = e.id
                where e.id = :1),
            (select * from empleados e
                join empleados_por_depto exd on exd.id_empleado = e.id
                join departamentos d on exd.id_departamento = d.id
                where e.id = :1 and d.nombre = 'recursos_humanos')
        from dual""", {id_empleado, "rrhh": NOMBRE_DEPTO_RRHH})

    if filas:
        es_gerente, es_encargado, es_rrhh = filas[0]

        if es_gerente: roles.add("gerente_depto")
        if es_encargado: roles.add("encargado_proyecto")
        if es_rrhh: roles.add("admin_rrhh")

    return roles

class Usuario():
    def __init__(self, nombre: str, correo: str, clave: str, roles : list = [], registrar: bool = True):
        self.nombre = nombre
        self.correo = correo
        self.clave = hashear_clave(clave)
        self.roles = roles
        self.sesion_activa = False

        if registrar:
            validar_tabla_usuarios()
            insertar_datos_usuario(self)

    def iniciar_sesion(self, correo: str, clave: str):
        if isinstance(correo, str) and isinstance(clave, str):
            usuario_in = iniciar_sesion_bd(correo, clave)
            self.roles = bd_calcular_roles()
            self = usuario_in
        return self

    def cerrar_sesion(self):
        self.sesion_activa = False
        print("[INFO] Sesión cerrada correctamente")

        return True

    def cambiar_contrasena(self, nueva_clave: str):
        if isinstance(nueva_clave, str):
            if bd_actualizar_clave(self, nueva_clave):
                self.clave = hashear_clave(nueva_clave)
        else:
            print("Clave inválida | No corresponde a tipo String")

    def tiene_rol(self, rol: str) -> bool:
        return rol in self.roles 