from model.usuario import Usuario
from model.empleado import Empleado
from model.adminrrhh import AdminRRHH

e_id = int(input("Ingrese el ID para el empleado:"))
e_nombre = str(input("Ingrese el nombre del empleado:"))
e_direccion = str(input("Ingrese la direccion del empleado:"))
e_fono = int(input("Ingrese el numero telefonico del empleado:"))
e_fecha_inicio = str(input("Ingrese la fecha de inicio segun contrato del empleado:"))
e_salario = int(input("Ingrese el salario para el empleado:"))

test_admin = AdminRRHH()
print(test_admin.registrar_empleado(e_id, e_nombre, e_direccion, e_fono, e_fecha_inicio, e_salario))