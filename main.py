from model.usuario import Usuario
from model.empleado import Empleado
from model.adminrrhh import AdminRRHH
from model.departamento import Departamento
from model.proyecto import Proyecto



"""
SECCION DE PRUEBAS:
"""
test_empleado = Empleado("pedro", "hola@mail.com", "qwerty", "abc123", 123, "01-02-1999", 500000)

test_admin = AdminRRHH("juan", "chao@mail.me", "xyz789", "Av. Nida", 958575, "27-02-2025", 150000)

test_admin.crear_departamento("Depto1", test_empleado)
