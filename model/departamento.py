from DataBase.queries import ejecutar_consulta
from .proyecto import Proyecto
from .empleado import Empleado


def validar_tabla_departamentos():
    consulta_sql = """
        create table if not exists departamentos (
            id_departamento NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre varchar2(100) not null unique,
            id_gerente number not null
        )
    """
    ejecutar_consulta(consulta_sql, (), "Tabla departamentos validada correctamente",
                      "Validación de tabla departamentos abortada")

def validar_datos_departamento(nombre, id_gerente):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre del departamento es obligatorio y debe ser String")
    if len(nombre.strip()) > 100:
        raise ValueError("El nombre no puede superar los 100 caracteres")
    if not isinstance(id_gerente, int) or isinstance(id_gerente, bool) or id_gerente <= 0:
        raise ValueError("El id del gerente debe ser un entero positivo")

ERR_NOMBRE_DUPLICADO = {1: "Ya existe un departamento con ese nombre"}  # ORA-00001
ERR_REGISTROS_ASOCIADOS = {2292: "No se puede eliminar: tiene registros asociados"}  # ORA-02292

class Departamento():
    def __init__(self, nombre: str, id_gerente: int):
        validar_datos_departamento(nombre, id_gerente)

        self.id_departamento = None
        self.nombre = nombre.strip()
        self.id_gerente = id_gerente

        validar_tabla_departamentos()
        self.id_departamento = ejecutar_consulta(
            "insert into departamentos (nombre, id_gerente) values (:1, :2) returning id_departamento into :3",
            (self.nombre, self.id_gerente), "Departamento insertado correctamente",
            "Departamento no registrado", errores_integridad=ERR_NOMBRE_DUPLICADO,
            retornar_id=True) or None

    def editar(self, nuevo_nombre: str, nuevo_id_gerente: int):
        validar_datos_departamento(nuevo_nombre, nuevo_id_gerente)

        if ejecutar_consulta(
                "update departamentos set nombre = :1, id_gerente = :2 where id_departamento = :3",
                (nuevo_nombre.strip(), nuevo_id_gerente, self.id_departamento),
                "Departamento actualizado correctamente", "Departamento no se pudo actualizar",
                "El departamento no existe en la base de datos", ERR_NOMBRE_DUPLICADO):
            self.nombre = nuevo_nombre.strip()
            self.id_gerente = nuevo_id_gerente

    def eliminar(self):
        return ejecutar_consulta(
            "delete from departamentos where id_departamento = :1", (self.id_departamento,),
            "Departamento eliminado correctamente", "Departamento no se pudo eliminar",
            "El departamento no existe en la base de datos", ERR_REGISTROS_ASOCIADOS)

    def crear_proyecto(self, p_nombre, p_descripcion, p_fecha_inicio):
        if self.id_departamento is None:
            print("[WARNING] El departamento no está registrado en la base de datos")
            return None

        nuevo_proyecto = Proyecto(p_nombre, p_descripcion, p_fecha_inicio, self.id_departamento)

        return nuevo_proyecto if nuevo_proyecto.id is not None else None

    def editar_proyecto(self, id_proyecto: int, p_nombre: str, p_descripcion: str, p_fecha_inicio: str):
        if not isinstance(id_proyecto, int):
            print("Id inválido | No corresponde a tipo Integer")
            return False

        return ejecutar_consulta(
            """update proyectos set nombre = :1, descripcion = :2,
                                    fecha_inicio = to_date(:3, 'YYYY-MM-DD')
               where id = :4 and id_departamento = :5""",
            (p_nombre, p_descripcion, p_fecha_inicio, id_proyecto, self.id_departamento),
            "Proyecto actualizado correctamente", "Proyecto no se pudo actualizar",
            "El proyecto no existe o no pertenece a este departamento")

    def eliminar_proyecto(self, id_proyecto: int):
        if not isinstance(id_proyecto, int):
            print("Id inválido | No corresponde a tipo Integer")
            return False

        return ejecutar_consulta(
            "delete from proyectos where id = :1 and id_departamento = :2",
            (id_proyecto, self.id_departamento), "Proyecto eliminado correctamente",
            "Proyecto no se pudo eliminar",
            "El proyecto no existe o no pertenece a este departamento", ERR_REGISTROS_ASOCIADOS)

    def asignar_empleado(self, empleado: Empleado):
        if not isinstance(empleado, Empleado):
            print("Empleado inválido | No corresponde a tipo Empleado")
            return False

        return ejecutar_consulta(
            "update empleados set id_departamento = :1 where correo = :2 and id_departamento is null",
            (self.id_departamento, empleado.correo), "Empleado asignado correctamente",
            "Empleado no se pudo asignar",
            "El empleado no existe o ya tiene un departamento asignado")

    def reasignar_empleado(self, empleado: Empleado, departamento_destino: "Departamento"):
        if not isinstance(empleado, Empleado):
            print("Empleado inválido | No corresponde a tipo Empleado")
            return False

        if not isinstance(departamento_destino, Departamento) or departamento_destino.id_departamento is None:
            print("Departamento destino inválido | No está registrado en la base de datos")
            return False

        return ejecutar_consulta(
            "update empleados set id_departamento = :1 where correo = :2 and id_departamento = :3",
            (departamento_destino.id_departamento, empleado.correo, self.id_departamento),
            "Empleado reasignado correctamente", "Empleado no se pudo reasignar",
            "El empleado no existe o no pertenece al departamento de origen")