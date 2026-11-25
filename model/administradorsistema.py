from config.app_config import conectar_db, oracledb
from .usuario import Usuario

ROLES_VALIDOS = ("admin_sistema", "admin_rrhh")

def bd_agregar_rol(correo: str, rol: str):
    consulta_insert = "insert into roles_usuario (correo, rol) values (:1, :2)"
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_insert, (correo, rol))
            conn.commit()

            print("[INFO] Rol agregado correctamente")
            return True
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] El usuario ya tiene ese rol")   # ORA-00001
        elif error.code == 2291:
            print("[WARNING] El usuario no existe")          # ORA-02291
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Rol no se pudo agregar | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return False

def bd_quitar_rol(correo: str, rol: str):
    consulta_delete = "delete from roles_usuario where correo = :1 and rol = :2"
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_delete, (correo, rol))

            if cursor.rowcount == 0:
                print("[WARNING] El usuario no tiene ese rol")
                return False

            conn.commit()
            print("[INFO] Rol quitado correctamente")
            return True
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Rol no se pudo quitar | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return False

class AdministradorDeSistema():
    def __init__(self, usuario: Usuario):
        if not usuario.tiene_rol("admin_sistema"):
            raise PermissionError("Se requiere el rol admin_sistema")

        self.usuario = usuario

    def agregar_rol(self, correo: str, rol: str):
        if rol not in ROLES_VALIDOS:
            print(f"[WARNING] Rol inválido | Opciones: {', '.join(ROLES_VALIDOS)}")
            return False

        return bd_agregar_rol(correo, rol)

    def quitar_rol(self, correo: str, rol: str):
        if correo == self.usuario.correo and rol == "admin_sistema":
            print("[WARNING] No puedes quitarte tu propio rol de administrador")
            return False

        return bd_quitar_rol(correo, rol)