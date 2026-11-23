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
