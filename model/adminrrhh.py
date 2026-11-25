from .departamento import Departamento
from .empleado import Empleado

class AdminRRHH():
    def __init__(self, usuario):
        if not (usuario.tiene_rol("admin_rrhh") or usuario.tiene_rol("admin_sistema")):
            raise PermissionError("No tiene permisos de RRHH")

        self.usuario = usuario

    def registrar_empleado(self, nombre: str, correo: str, clave: str, direccion: str, telefono: int,
                           fecha_inicio_contrato: str, salario: int, id_departamento: int = None) -> str:
        empleado = Empleado(nombre, correo, clave, direccion, telefono,
                            fecha_inicio_contrato, salario, id_departamento)

        return f"Empleado {nombre} registrado" if empleado.registrado else f"Empleado {nombre} no registrado"

    def generar_informe(self):
        pass

    def crear_departamento(self, nombre: str, id_gerente: int = None):
        departamento = Departamento(nombre, id_gerente)

        return departamento if departamento.id_departamento is not None else None

    def listar_departamentos(self):
        return Departamento.listar()

    def editar_departamento(self, departamento: Departamento, nuevo_nombre: str, nuevo_id_gerente: int = None):
        return departamento.editar(nuevo_nombre, nuevo_id_gerente)

    def eliminar_departamento(self, departamento: Departamento):
        return departamento.eliminar()