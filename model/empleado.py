from .usuario import Usuario
from .registrohorario import RegistroHorario
class Empleado(Usuario):
    def __init__(self, nombre: str, direccion: str, telefono: int, correo: str, clave: str, fecha_inicio_contrato: str, salario: int):
        super().__init__(nombre, correo, clave)
        self.direccion = direccion
        self.telefono = telefono
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario

    def registrar_horas(self, p_fecha: str, p_horas_trabajadas: float, p_desc_tareas: str):
        nuevo_registro = RegistroHorario(self,
                                         p_fecha,
                                         p_horas_trabajadas,
                                         p_desc_tareas) #Al integrar BBDD esto se cambiara
                                                        #Para usar de forma automatica el
                                                        #proyecto al que este asignado el empleado

        #return tambien sujeto a cambio (placeholder)
        return f"{p_horas_trabajadas}hrs registradas a nombre de {self.nombre}"