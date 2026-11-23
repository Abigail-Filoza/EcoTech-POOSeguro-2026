from model.usuario import Usuario
from model.empleado import Empleado
from model.proyecto import Proyecto

"""
SECCION DE PRUEBAS:
"""
# e_nombre = str(input("nombre: "))
# e_direccion = str(input("direccion: "))
# e_fono = int(input("telefono: "))
# e_correo = str(input("correo: "))
# e_clave = str(input("clave: "))
# e_fecha_inicio = str(input("fecha inicio contrato: "))
# e_salario = int(input("Ingrese el salario para el empleado:"))

# test_admin = AdminRRHH("Sofia", "Av. Xyz", 987, "hola@email.com", "qwerty", "01-01-2025", 500000)
# print(test_admin.registrar_empleado(e_nombre,
#                                     e_direccion,
#                                     e_fono, e_correo,
#                                     e_clave,
#                                     e_fecha_inicio,
#                                     e_salario))

# print(test_admin.nombre)

#test_usuario = Usuario("pedro", "hola@mail.me", "abc123")

test_empleado = Empleado("juan", "chao@mail.me", "xyz789", "Av. Nida", 958575, "27-FEB-2025", 150000)

test_proyecto = Proyecto("Proyecto 1", "Prueba de proyecto", "01-JAN-2025", test_empleado)

test_proyecto.asignar_empleado(test_empleado)

test_empleado.registrar_horas("01-APR-2025", 7.75, "y, nse", test_proyecto)

test_proyecto.deasignar_empleado(test_empleado)