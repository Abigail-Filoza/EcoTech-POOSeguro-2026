from DataBase.queries import ejecutar_consulta, consultar

def validar_tabla_proyectos():
    consulta_sql = """
        create table if not exists proyectos (
            id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre varchar2(100) not null,
            descripcion varchar2(255),
            fecha_inicio date not null,
            id_departamento number not null,
            id_encargado number,
            constraint fk_proyecto_departamento foreign key (id_departamento)
                references departamentos(id_departamento),
            constraint fk_proyecto_encargado foreign key (id_encargado) references usuarios(id)
        )
    """
    ejecutar_consulta(consulta_sql, (), "Tabla proyectos validada correctamente",
                      "Validación de tabla proyectos abortada")

def validar_datos_proyecto(nombre, descripcion, fecha_inicio):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre del proyecto es obligatorio y debe ser String")
    if len(nombre.strip()) > 100:
        raise ValueError("El nombre no puede superar los 100 caracteres")
    if not isinstance(descripcion, str) or len(descripcion) > 255:
        raise ValueError("La descripción debe ser String de hasta 255 caracteres")
    if not isinstance(fecha_inicio, str) or not fecha_inicio.strip():
        raise ValueError("La fecha de inicio es obligatoria (YYYY-MM-DD)")

def proyectos_desde_filas(filas):
    return [Proyecto(nombre, descripcion or "", fecha, id_dep, id_enc, registrar=False, id_proyecto=id_proy)
            for id_proy, nombre, descripcion, fecha, id_dep, id_enc in filas]

SELECT_PROYECTOS = """select id, nombre, descripcion, to_char(fecha_inicio, 'YYYY-MM-DD'),
                             id_departamento, id_encargado from proyectos"""

class Proyecto():
    def __init__(self, nombre: str, descripcion: str, fecha_inicio: str, id_departamento: int,
                 id_encargado: int = None, registrar: bool = True, id_proyecto: int = None):
        validar_datos_proyecto(nombre, descripcion, fecha_inicio)

        self.id = id_proyecto
        self.nombre = nombre.strip()
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio  # formato YYYY-MM-DD
        self.id_departamento = id_departamento
        self.id_encargado = id_encargado

        if registrar:  
            self.id = ejecutar_consulta(
                """insert into proyectos (nombre, descripcion, fecha_inicio, id_departamento, id_encargado)
                   values (:1, :2, to_date(:3, 'YYYY-MM-DD'), :4, :5) returning id into :6""",
                (self.nombre, self.descripcion, self.fecha_inicio, self.id_departamento, self.id_encargado),
                "Proyecto insertado correctamente", "Proyecto no registrado",
                errores_integridad={2291: "El departamento o el encargado no existe"},
                retornar_id=True) or None

    @staticmethod
    def listar_por_departamento(id_departamento: int):
        return proyectos_desde_filas(consultar(
            SELECT_PROYECTOS + " where id_departamento = :1 order by id", (id_departamento,)))

    @staticmethod
    def listar_por_encargado(id_usuario: int):
        return proyectos_desde_filas(consultar(
            SELECT_PROYECTOS + " where id_encargado = :1 order by id", (id_usuario,)))

    def listar_empleados(self):
        """Devuelve [(correo, nombre)] de los empleados asignados al proyecto."""
        return consultar("""select u.correo, u.nombre from empleados e
                            join usuarios u on u.id = e.id_usuario
                            where e.id_proyecto = :1""", (self.id,))

    def asignar_empleado(self, correo: str):
        # Solo empleados del mismo departamento del proyecto
        return ejecutar_consulta(
            """update empleados set id_proyecto = :1
               where id_usuario = (select id from usuarios where correo = :2)
                 and id_departamento = :3""",
            (self.id, correo, self.id_departamento), "Empleado asignado al proyecto correctamente",
            "Empleado no se pudo asignar",
            "El empleado no existe o no pertenece al departamento del proyecto")

    def desasignar_empleado(self, correo: str):
        return ejecutar_consulta(
            """update empleados set id_proyecto = null
               where id_usuario = (select id from usuarios where correo = :1)
                 and id_proyecto = :2""",
            (correo, self.id), "Empleado quitado del proyecto correctamente",
            "Empleado no se pudo desasignar", "El empleado no está asignado a este proyecto")