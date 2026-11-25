import os

import oracledb
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("ORACLE_USER")
DB_PASS = os.getenv("ORACLE_PASSWORD")
DB_DSN = os.getenv("ORACLE_DSN")

def conectar_db():
    try:
        conexion = oracledb.connect(user = DB_USER, password = DB_PASS, dsn= DB_DSN)
        return conexion
    except oracledb.Error as error:
        print(f"[ERROR] Conexión a Oracle FreeSQL | {error}")
    
NOMBRE_DEPTO_RRHH = "Recursos Humanos"