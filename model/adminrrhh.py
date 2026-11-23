from utils.metodos_bd import ejecutar_consulta
from .empleado import Empleado
from .departamento import Departamento, validar_datos_departamento



ERR_NOMBRE_DUPLICADO = {1: "Ya existe un departamento con ese nombre"}  # ORA-00001
ERR_REGISTROS_ASOCIADOS = {2292: "No se puede eliminar: tiene registros asociados"}  # ORA-02292

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

    def editar_departamento(self, depto: Departamento, nuevo_nombre: str, nuevo_id_gerente: int):
        validar_datos_departamento(nuevo_nombre, nuevo_id_gerente)

        if ejecutar_consulta(
                "update departamentos set nombre = :1, id_gerente = :2 where id_departamento = :3",
                (nuevo_nombre.strip(), nuevo_id_gerente, depto.id_departamento),
                "Departamento actualizado correctamente", "Departamento no se pudo actualizar",
                "El departamento no existe en la base de datos", ERR_NOMBRE_DUPLICADO):
            depto.nombre = nuevo_nombre.strip()
            depto.id_gerente = nuevo_id_gerente

    def eliminar_departamento(self, depto: Departamento):
        return ejecutar_consulta(
            "delete from departamentos where id_departamento = :1", (depto.id_departamento,),
            "Departamento eliminado correctamente", "Departamento no se pudo eliminar",
            "El departamento no existe en la base de datos", ERR_REGISTROS_ASOCIADOS)