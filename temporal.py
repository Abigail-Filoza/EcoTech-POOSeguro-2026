from config.app_config import conectar_db

conn = conectar_db()
cursor = conn.cursor()
cursor.execute("alter table empleados add id_proyecto number")
cursor.execute("""alter table empleados add constraint fk_empleado_proyecto
                  foreign key (id_proyecto) references proyectos(id)""")
cursor.close()
conn.close()
print("Listo")