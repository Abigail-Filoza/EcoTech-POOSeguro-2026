import bcrypt

def pedir_entero(texto: str):
    try:
        return int(input(texto))
    except ValueError:
        print(" Debe ingresar un número entero.")
        return None

def hashear_clave(clave: str) -> str:
    clave_bytes = clave.encode('utf-8')
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode('utf-8')