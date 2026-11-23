from .empleado import Empleado
from .departamento import Departamento



class AdminRRHH(Empleado):
    
    def registrar_empleado(self, e_nombre: str, e_direccion: str, e_fono: int, e_correo: str, e_clave: str, e_fecha_inicio: str, e_salario: int):
        
        nuevo_empleado = Empleado(e_nombre,
                                  e_direccion,
                                  e_fono,
                                  e_correo,
                                  e_clave,
                                  e_fecha_inicio,
                                  e_salario)
        
        return f"Empleado {e_nombre} ({e_correo}) registrado. Contrato efectivo desde {e_fecha_inicio}"

    def generar_informe():
        pass

    def crear_departamento(self, d_nombre, d_id_gerente):
        nuevo_depto = Departamento(d_nombre, d_id_gerente)

    def editar_departamento():
        pass #este metodo solo tiene real sentido con la bbdd integrada

    def eliminar_departamento():
        pass #este metodo solo tiene real sentido con la bbdd integrada