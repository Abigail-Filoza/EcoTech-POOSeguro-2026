from __future__ import annotations
import hashlib
import hmac
import os
from config.app_config import conectar_db, oracledb

def hashear_clave(clave: str) -> str:
    salt = os.urandom(16)
    hash_clave = hashlib.pbkdf2_hmac("sha256", clave.encode(), salt, 200_000)

    return f"{salt.hex()}${hash_clave.hex()}"  

def verificar_clave(clave: str, clave_guardada: str) -> bool:
    try:
        salt_hex, hash_hex = clave_guardada.split("$")
        hash_clave = hashlib.pbkdf2_hmac("sha256", clave.encode(), bytes.fromhex(salt_hex), 200_000)
    except ValueError:
        return False  # la clave guardada no tiene formato de hash (por ejemplo, texto plano antiguo)

    return hmac.compare_digest(hash_clave.hex(), hash_hex)

def bd_buscar_usuario(correo: str):
    consulta_select = "select nombre, clave from usuarios where correo = :1"
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_select, (correo,))

            return cursor.fetchone()  # (nombre, clave) o None si no existe
    except Exception as e:
        print(f"[ERROR] Búsqueda de usuario fallida | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return None

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
            cursor.execute(consulta_insert, (usuario.nombre, usuario.correo, hashear_clave(usuario.clave)))
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
        self.sesion_activa = False

        if registrar:  # False cuando solo reconstruimos un usuario que ya existe (login)
            validar_tabla_usuarios()
            insertar_datos_usuario(self)

    @staticmethod
    def iniciar_sesion(correo: str, clave: str):
        """Devuelve el Usuario si las credenciales son correctas, o None si no."""
        if not isinstance(correo, str) or not isinstance(clave, str) or not correo.strip() or not clave:
            print("Credenciales inválidas | Correo y clave deben ser String no vacíos")
            return None

        fila = bd_buscar_usuario(correo.strip())

        if fila and verificar_clave(clave, fila[1]):
            usuario = Usuario(fila[0], correo.strip(), fila[1], registrar=False)  # fila[1] es el hash
            usuario.sesion_activa = True
            print("[INFO] Sesión iniciada correctamente")

            return usuario

        print("[WARNING] Correo o contraseña incorrectos")  # mismo mensaje para ambos casos, a propósito

        return None

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