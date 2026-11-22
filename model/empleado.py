from .usuario import Usuario
class Empleado(Usuario):
    def __init__(self, id: int, nombre: str, direccion: str, telefono: int, correo: str, fecha_inicio_contrato: str, salario: int):
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario

    def registrar_horas():
        return "string" #placeholder para asegurar tipo de dato