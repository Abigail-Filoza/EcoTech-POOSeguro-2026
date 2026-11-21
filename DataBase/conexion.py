import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

class ConexionOracle:
    def __init__(self):
        self.user = os.getenv("ORACLE_USER")
        self.password = os.getenv("ORACLE_PASSWORD")
        self.dsn = os.getenv("ORACLE_DSN")

    def conectar(self):
        try:
            conexion = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn
            )
            return conexion
        except oracledb.Error as error:
            print(f"Error al conectar a Oracle FreeSQL: {error}")
            return None

if __name__ == "__main__":
    db = ConexionOracle()
    conn = db.conectar()
    if conn:
        print("¡Conexión exitosa a Oracle FreeSQL!")
        conn.close()
