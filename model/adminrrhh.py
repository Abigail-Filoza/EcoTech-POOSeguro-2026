from .departamento import Departamento

class AdminRRHH():
    def __init__(self, usuario):
        if not usuario.tiene_rol("admin_rrhh"):
            raise PermissionError("Se requiere el rol admin_rrhh")

        self.usuario = usuario

    def registrar_empleado(self):
        return "string" # placeholder para asegurar tipo de dato

    def generar_informe(self):
        pass

    def crear_departamento(self, nombre: str, id_gerente: int):
        departamento = Departamento(nombre, id_gerente)

        return departamento if departamento.id_departamento is not None else None  # None si el insert falló

    def editar_departamento(self, departamento: Departamento, nuevo_nombre: str, nuevo_id_gerente: int):
        departamento.editar(nuevo_nombre, nuevo_id_gerente)

    def eliminar_departamento(self, departamento: Departamento):
        return departamento.eliminar()