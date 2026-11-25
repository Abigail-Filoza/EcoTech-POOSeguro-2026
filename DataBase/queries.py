from config.app_config import conectar_db, oracledb

def ejecutar_consulta(consulta, parametros, msg_ok, msg_error, msg_sin_filas=None,
                      errores_integridad=None, retornar_id=False):
    """Ejecuta una consulta DML/DDL. Devuelve True (o el id si retornar_id) o False si falla."""
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            if retornar_id:
                id_generado = cursor.var(int)
                parametros = (*parametros, id_generado)

            cursor.execute(consulta, parametros)

            if msg_sin_filas and cursor.rowcount == 0:
                print(f"[WARNING] {msg_sin_filas}")
                return False

            conn.commit()
            print(f"[INFO] {msg_ok}")
            return id_generado.getvalue()[0] if retornar_id else True
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        mensaje = (errores_integridad or {}).get(e.args[0].code)
        print(f"[WARNING] {mensaje}" if mensaje else f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] {msg_error} | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return False

def consultar(consulta, parametros=()):
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