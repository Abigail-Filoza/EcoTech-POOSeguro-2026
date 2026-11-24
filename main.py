from view.menus import menu_principal, menu_usuario

def main():
    programa_activo = True
    usuario = None

    while programa_activo:
        if usuario:  # hay sesión iniciada: menú del usuario
            usuario = menu_usuario(usuario)
        else:  # sin sesión: menú principal
            usuario, programa_activo = menu_principal(usuario)

if __name__ == "__main__":
    main()

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

