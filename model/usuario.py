import bcrypt
from config.app_config import conectar_db, oracledb

def hashear_clave(clave: str) -> str:
    clave_bytes = clave.encode('utf-8')
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode('utf-8')

def validar_tabla_roles():
    consulta_sql = """
        create table if not exists roles_usuario (
            correo varchar2(100) not null,
            rol varchar2(30) not null,
            constraint uq_rol_usuario unique (correo, rol),
            constraint fk_rol_usuario foreign key (correo)
                references usuarios(correo) on delete cascade
        )
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_sql)
            print("[INFO] Tabla roles_usuario validada correctamente")
    except Exception as e:
        print(f"[ERROR] Validación de tabla roles_usuario abortada | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def bd_cargar_roles(correo: str) -> set:
    consulta_select = "select rol from roles_usuario where correo = :1"
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_select, (correo,))

            return {fila[0] for fila in cursor.fetchall()}
    except Exception as e:
        print(f"[ERROR] No se pudieron cargar los roles | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return set()

def validar_tabla_usuarios():
    consulta_sql = """
        create table if not exists usuarios (
            id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre varchar2(100) not null,
            correo varchar2(100) not null unique,
            clave varchar2(150) not null
        )
    """
    conn = None
    cursor = None

    try:
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

def insertar_datos_usuario(usuario: "Usuario"):
    consulta_insert = """insert into usuarios (nombre, correo, clave)
                         values (:1, :2, :3)"""
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_insert, (usuario.nombre, usuario.correo,
                                             hashear_clave(usuario.clave)))
            conn.commit()

            print("[INFO] Usuario insertado correctamente")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] Este correo ya está en uso") # ORA-00001
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Usuario no registrado | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def iniciar_sesion(correo: str, clave: str):
    """
        Recibe el correo y la contraseña y los valida con la base de datos.
        En caso de ser correctos, retorna el usuario (con su rol).
        En caso incorrecto devuelve False.
    """
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
                    usuario = Usuario(nombre, correo, clave_bd, registrar=False)
                    validar_tabla_roles()
                    usuario.roles = bd_cargar_roles(correo)
                    usuario.sesion_activa = True
                    return usuario

            print("[ERROR] Credenciales incorrectas")
            return False
        else:
            print("[ERROR] No se pudo conectar la bd")
            return False
    except Exception as e:
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

class Usuario():
    def __init__(self, nombre: str, correo: str, clave: str, registrar: bool = True):
        self.nombre = nombre
        self.correo = correo
        self.clave = clave
        self.roles = set() 
        self.sesion_activa = False

        if registrar:  # False cuando solo reconstruimos un usuario que ya existe (login)
            validar_tabla_usuarios()
            insertar_datos_usuario(self)
    
    def tiene_rol(self, rol: str) -> bool:
        return rol in self.roles 

    def cerrar_sesion(self):
        self.sesion_activa = False
        print("[INFO] Sesión cerrada correctamente")

        return True

    def cambiar_contrasena(self, nueva_clave: str):
        if isinstance(nueva_clave, str) and nueva_clave:
            if bd_actualizar_clave(self, nueva_clave):
                self.clave = hashear_clave(nueva_clave)
        else:
            print("Clave inválida | No corresponde a tipo String")