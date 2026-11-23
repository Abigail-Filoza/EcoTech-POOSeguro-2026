from .empleado import Empleado
from .proyecto import Proyecto

class RegistroHorario():
    def __init__(self, empleado: Empleado, fecha: str, horas_trabajadas: float, desc_tareas: str, proyecto: Proyecto):
        self.empleado = empleado
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.desc_tareas = desc_tareas
        self.proyecto = proyecto