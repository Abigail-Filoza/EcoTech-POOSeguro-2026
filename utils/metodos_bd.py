from config.app_config import conectar_db, oracledb

def ejecutar_consulta(consulta: str, parametros: tuple | None, msg_ok: str, msg_error: str, errores_posibles: dict[int, str] = None):
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            if parametros != None:
                cursor.execute(consulta, parametros)
            else:
                cursor.execute(consulta)

            conn.commit()
            print(f"[INFO] {msg_ok}")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        if errores_posibles != None:
            error = e.args[0]

            for codigo, texto in errores_posibles.items():
                if error == codigo:
                    print(f"[ERROR] {texto}")
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] {msg_error} | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def consultar_id_empleado(correo_empleado: str):
    from model.usuario import Usuario
    from model.empleado import Empleado

    if isinstance(correo_empleado, str):
        consulta_select_usuario = """
            select id from usuarios
            where usuarios.correo = :1;
        """
    
        consulta_select_empleado = """
            select id from empleados
            where empleados.id_usuario = :1;
        """

        conn = None
        cursor = None
    
        try:
            conn = conectar_db()
    
            if conn:
                cursor = conn.cursor()
    
                cursor.execute(consulta_select_usuario, (correo_empleado,))
                id_usuario = str(cursor.fetchone()[0])
    
                cursor.execute(consulta_select_empleado, (id_usuario,))
                id_empleado = str(cursor.fetchone()[0])
    
                return id_empleado
        except oracledb.IntegrityError as e:
            if conn:
                conn.rollback() # Si algo falla, nos aseguramos de que nada cambie en la bd
    
            print(f"[ERROR] Error de integridad | {e}")
        except Exception as e:
            if conn:
                conn.rollback()
    
            print(f"[ERROR] No se logro hacer consulta | {e}")
        finally:
            if cursor:
                cursor.close()
    
            if conn:
                conn.close()

def consultar(consulta: str, parametros: tuple =()):
    """Ejecuta un SELECT y devuelve la lista de filas (vacía si falla)."""
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta, parametros)

            return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] Consulta fallida | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return []