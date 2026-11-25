from DataBase.queries import ejecutar_consulta, consultar 
from .proyecto import Proyecto, validar_datos_proyecto
from config.app_config import NOMBRE_DEPTO_RRHH


def validar_tabla_departamentos():
    consulta_sql = """
        create table if not exists departamentos (
            id_departamento NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre varchar2(100) not null unique,
            id_gerente number,
            constraint fk_departamento_gerente foreign key(id_gerente) references usuarios(id)
        )
    """
    ejecutar_consulta(consulta_sql, (), "Tabla departamentos validada correctamente",
                      "Validación de tabla departamentos abortada")

def validar_datos_departamento(nombre, id_gerente):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre del departamento es obligatorio y debe ser String")
    if len(nombre.strip()) > 100:
        raise ValueError("El nombre no puede superar los 100 caracteres")
    if id_gerente is not None and (not isinstance(id_gerente, int) or isinstance(id_gerente, bool) or id_gerente <= 0):
        raise ValueError("El id del gerente debe ser un entero positivo o quedar vacío")

ERR_NOMBRE_DUPLICADO = {1: "Ya existe un departamento con ese nombre"}  # ORA-00001
ERR_REGISTROS_ASOCIADOS = {2292: "No se puede eliminar: tiene registros asociados"}  # ORA-02292

class Departamento():
    def __init__(self, nombre: str, id_gerente: int = None, registrar: bool = True, id_departamento: int = None):
        validar_datos_departamento(nombre, id_gerente)

        self.id_departamento = self.id_departamento
        self.nombre = nombre.strip()
        self.id_gerente = id_gerente

        if registrar: 
            self.id_departamento = ejecutar_consulta(
            "insert into departamentos (nombre, id_gerente) values (:1, :2) returning id_departamento into :3",
            (self.nombre, self.id_gerente), "Departamento insertado correctamente",
            "Departamento no registrado", errores_integridad=ERR_NOMBRE_DUPLICADO,
            retornar_id=True) or None
            
    @staticmethod
    def listar_por_gerente(id_usuario: int):
        filas = consultar("""select id_departamento, nombre, id_gerente from departamentos
                             where id_gerente = :1 order by id_departamento""", (id_usuario,))

        return [Departamento(nombre, id_gerente, registrar=False, id_departamento=id_dep)
                for id_dep, nombre, id_gerente in filas]

    def listar_proyectos(self):
        return Proyecto.listar_por_departamento(self.id_departamento)

    def crear_proyecto(self, p_nombre: str, p_descripcion: str, p_fecha_inicio: str, id_encargado: int = None):
        nuevo_proyecto = Proyecto(p_nombre, p_descripcion, p_fecha_inicio, self.id_departamento, id_encargado)

        return nuevo_proyecto if nuevo_proyecto.id is not None else None

    def editar_proyecto(self, id_proyecto: int, p_nombre: str, p_descripcion: str,
                        p_fecha_inicio: str, id_encargado: int = None):
        validar_datos_proyecto(p_nombre, p_descripcion, p_fecha_inicio)

        return ejecutar_consulta(
            """update proyectos set nombre = :1, descripcion = :2,
                                    fecha_inicio = to_date(:3, 'YYYY-MM-DD'), id_encargado = :4
               where id = :5 and id_departamento = :6""",
            (p_nombre.strip(), p_descripcion, p_fecha_inicio, id_encargado, id_proyecto, self.id_departamento),
            "Proyecto actualizado correctamente", "Proyecto no se pudo actualizar",
            "El proyecto no existe o no pertenece a este departamento")

    def eliminar_proyecto(self, id_proyecto: int):
        return ejecutar_consulta(
            "delete from proyectos where id = :1 and id_departamento = :2",
            (id_proyecto, self.id_departamento), "Proyecto eliminado correctamente",
            "Proyecto no se pudo eliminar",
            "El proyecto no existe o no pertenece a este departamento",
            {2292: "No se puede eliminar: el proyecto tiene empleados asignados"})

    def asignar_empleado(self, correo: str):
        return ejecutar_consulta(
            """update empleados set id_departamento = :1
               where id_usuario = (select id from usuarios where correo = :2) and id_departamento is null""",
            (self.id_departamento, correo), "Empleado asignado correctamente", "Empleado no se pudo asignar",
            "El empleado no existe o ya tiene un departamento asignado")

    def reasignar_empleado(self, correo: str, departamento_destino: "Departamento"):
        # Al cambiar de departamento, el empleado sale de su proyecto actual
        return ejecutar_consulta(
            """update empleados set id_departamento = :1, id_proyecto = null
               where id_usuario = (select id from usuarios where correo = :2) and id_departamento = :3""",
            (departamento_destino.id_departamento, correo, self.id_departamento),
            "Empleado reasignado correctamente", "Empleado no se pudo reasignar",
            "El empleado no existe o no pertenece a este departamento")