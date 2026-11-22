class RegistroHorario():
    def __init__(self, id: int, id_empleado: int, fecha: str, horas_trabajadas: float, desc_tareas: str, id_proyecto: int):
        self.id = id
        self.id_empleado = id_empleado
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.desc_tareas = desc_tareas
        self.id_proyecto = id_proyecto