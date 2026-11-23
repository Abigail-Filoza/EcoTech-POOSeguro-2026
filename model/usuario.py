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

def bd_actualizar_clave(usuario: Usuario, nueva_clave: str):
    consulta_update = """
        update clientes set clave = :1
        where correo = :2
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_update, (nueva_clave, usuario.correo))
            conn.commit()

            print("[INFO] Clave actualizada correctamente")
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

class Usuario():
    def __init__(self, nombre: str, correo: str, clave: str):
        self.nombre = nombre
        self.correo = correo
        self.clave = clave

        validar_tabla_usuarios()
        insertar_datos_usuario(self)

    def iniciar_sesion(correo: str, clave: str):
        bool_var = True # placeholder para asegurar el uso de un valor
        return bool_var # booleano en la funcion una vez escrita

    def cerrar_sesion():
        bool_var = True # placeholder para asegurar el uso de un valor
        return bool_var # booleano en la funcion una vez escrita

    def cambiar_contrasena(self, nueva_clave: str):
        if isinstance(nueva_clave, str):
            bd_actualizar_clave(self, nueva_clave)

            self.clave = nueva_clave
        else:
            print("Clave inválida | No corresponde a tipo String")