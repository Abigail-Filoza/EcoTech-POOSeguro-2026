from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .proyecto import Proyecto

class RegistroHorario():
    def __init__(self, fecha: str, horas_trabajadas: float, desc_tareas: str, proyecto: Proyecto):
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.desc_tareas = desc_tareas
        self.proyecto = proyecto