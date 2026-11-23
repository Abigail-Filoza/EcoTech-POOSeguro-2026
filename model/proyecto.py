from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .empleado import Empleado
class Proyecto():
    def __init__(self, nombre: str, descripcion: str, fecha_inicio: str):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio

    def asignar_empleado(self, empleado: Empleado):
        #este metodo solo tiene real sentido con integracion a bbdd
        print(f"Empleado {empleado.nombre} asignado a proyecto {self.nombre}.")