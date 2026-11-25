from config.app_config import conectar_db

conn = conectar_db()
cursor = conn.cursor()
cursor.execute("insert into roles_usuario (correo, rol) values (:1, :2)",
               ("bryan@gmail.com", "admin_sistema"))
conn.commit()  # sin commit, el insert se pierde
cursor.close()
conn.close()
print("Rol asignado")