import bcrypt
from config.app_config import conectar_db, oracledb

def hashear_clave(clave: str) -> str:
    clave_bytes = clave.encode('utf-8')
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode('utf-8')

def validar_tabla_usuarios():
    consulta_sql = """
        create table if not exists usuarios (
            id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre varchar2(100) not null,
            correo varchar2(100) not null unique,
            clave varchar2(150) not null,
            rol varchar2(30) default 'usuario' not null
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
    consulta_insert = """insert into usuarios (nombre, correo, clave, rol)
                         values (:1, :2, :3, :4)"""
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_insert, (usuario.nombre, usuario.correo,
                                             hashear_clave(usuario.clave), usuario.rol))
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
    consulta = "select nombre, clave, rol from usuarios where correo = :1"
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta, (correo,))
            datos_usuario = cursor.fetchone()  # (nombre, clave, rol) o None

            if datos_usuario:
                nombre, clave_bd, rol = datos_usuario

                # Se deben transformar ambas claves a bytes para validarlas
                if bcrypt.checkpw(clave.encode('utf-8'), str(clave_bd).encode('utf-8')):
                    print("[INFO] Ingreso correcto")
                    usuario = Usuario(nombre, correo, clave_bd, rol, registrar=False)
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
    def __init__(self, nombre: str, correo: str, clave: str, rol: str = "usuario", registrar: bool = True):
        self.nombre = nombre
        self.correo = correo
        self.clave = clave
        self.rol = rol
        self.sesion_activa = False

        if registrar:  # False cuando solo reconstruimos un usuario que ya existe (login)
            validar_tabla_usuarios()
            insertar_datos_usuario(self)

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