from view.menus import menu_inicial, menu_usuario

def main():
    programa_activo = True
    usuario = None

    while programa_activo:
        if usuario:  # hay sesión iniciada: menú del usuario
            usuario = menu_usuario(usuario)
        else:  # sin sesión: menú principal
            usuario, programa_activo = menu_inicial(usuario)

if __name__ == "__main__":
    main()



"""
SECCION DE PRUEBAS:
"""
# from model.usuario import Usuario
# from model.empleado import Empleado
# from model.adminrrhh import AdminRRHH
# from model.departamento import Departamento
# from model.proyecto import Proyecto

# usuario_bd = Usuario("Laura", "mail.com", "asdf")

# usuario_aux = Usuario("test","test","test",[],False)

# in_correo = input("correo: ")
# in_clave = input("clave: ")

# usuario_aux = usuario_aux.iniciar_sesion(in_correo,in_clave)

# print(usuario_aux.nombre)