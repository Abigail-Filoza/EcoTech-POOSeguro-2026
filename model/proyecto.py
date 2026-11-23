from .empleado import Empleado

class Proyecto():
    def __init__(self, nombre: str, descripcion: str, fecha_inicio: str, encargado: Empleado):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.encargado = encargado

    def asignar_empleado(self, empleado: Empleado):
        print(f"Empleado {empleado.nombre} asignado a proyecto {self.nombre}.")

    def deasignar_empleado(self, empleado: Empleado):
        pass