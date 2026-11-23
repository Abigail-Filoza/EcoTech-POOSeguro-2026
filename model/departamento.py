from .proyecto import Proyecto

class Departamento():
    def __init__(self, nombre: str, id_gerente: int):
        self.nombre = nombre
        self.id_gerente = id_gerente

    def crear_proyecto(self, p_nombre, p_descripcion, p_fecha_inicio):
        nuevo_proyecto = Proyecto(p_nombre, p_descripcion, p_fecha_inicio)

    def editar_proyecto():
        pass #este metodo solo tiene real sentido con la bbdd integrada

    def eliminar_proyecto():
        pass #este metodo solo tiene real sentido con la bbdd integrada

    def asignar_empleado():
        pass #este metodo solo tiene real sentido con la bbdd integrada

    def reasignar_empleado():
        pass #este metodo solo tiene real sentido con la bbdd integrada