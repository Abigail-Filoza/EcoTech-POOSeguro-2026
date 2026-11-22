from .empleado import Empleado
class AdminRRHH(Empleado):
    def __init__(self):
        pass

    def registrar_empleado(e_id: int, e_nombre: str, e_direccion: str, e_fono: int, e_correo: str, e_fecha_inicio: str, e_salario: int):
        
        nuevo_empleado = Empleado(e_id,
                                  e_nombre,
                                  e_direccion,
                                  e_fono,
                                  e_correo,
                                  e_fecha_inicio,
                                  e_salario)
        
        return f"Empleado #{nuevo_empleado.id}: {nuevo_empleado.nombre} registrado con fecha inicio {nuevo_empleado.fecha_inicio_contrato}"

    def generar_informe():
        pass

    def crear_departamento():
        pass

    def editar_departamento():
        pass

    def eliminar_departamento():
        pass

"""
Empleado ():
    id : int
    nombre : str
    direccion : str
    telefono : int
    correo: str
    fecha_inicio_contrato : str
    salario : int
"""