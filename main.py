from getpass import getpass
from model.usuario import Usuario

def pedir_login(max_intentos: int = 3):
    for intento in range(1, max_intentos + 1):
        correo = input("  Ingrese su correo     : ")
        clave = getpass("  Ingrese su contraseña : ")  # no muestra lo que escribes

        usuario = Usuario.iniciar_sesion(correo, clave)

        if usuario:
            return usuario

        print(f"  Intento {intento} de {max_intentos}")

    print("Demasiados intentos fallidos")
    return None

def main():
    usuario = pedir_login()

    if usuario is None:
        return

    print(f"\n  Bienvenido, {usuario.nombre}")

    while True:
        opcion = input("\n  1. Cambiar contraseña\n  2. Cerrar sesión\n  Opción: ")

        if opcion == "1":
            nueva = getpass("  Nueva contraseña : ")
            usuario.cambiar_contrasena(nueva)
        elif opcion == "2":
            usuario.cerrar_sesion()
            break
        else:
            print("[WARNING] Opción inválida")

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

test_usuario = Usuario("pedro", "hola@mail.me", "abc123")