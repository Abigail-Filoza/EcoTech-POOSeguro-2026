from utils.metodos_bd import ejecutar_consulta
from config.app_config import conectar_db, oracledb
from .empleado import Empleado
from .departamento import Departamento, update_datos_bd, validar_datos_departamento

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

    def crear_departamento(self, d_nombre: str, d_gerente: Empleado):
        nuevo_depto = Departamento(d_nombre, d_gerente)

    def editar_departamento(self, depto: Departamento, nuevo_nombre: str, nuevo_gerente: Empleado):
        validar_datos_departamento(nuevo_nombre, nuevo_gerente)

        ERR_NOMBRE_DUPLICADO = {1: "Ya existe un departamento con ese nombre"}  # ORA-00001

        nombre_ref = depto.nombre

        depto.nombre = nuevo_nombre
        depto.gerente = nuevo_gerente

        update_datos_bd(depto, nombre_ref)

    def eliminar_departamento(self, depto: Departamento):
        ERR_REGISTROS_ASOCIADOS = {2292: "No se puede eliminar: tiene registros asociados"}  # ORA-02292
        
        return ejecutar_consulta(
            "delete from departamentos where nombre = :1", (depto.nombre,),
            "Departamento eliminado correctamente", "Departamento no se pudo eliminar",
            "El departamento no existe en la base de datos", ERR_REGISTROS_ASOCIADOS)