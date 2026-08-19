# Importa la librería pwdlib, que sirve para manejar contraseñas de forma segura
from pwdlib import PasswordHash 

# Crea un objeto PasswordHash con la configuración recomendada (usa algoritmos seguros como Argon2 y Bcrypt)
password_hash = PasswordHash.recommended()

# Función para convertir una contraseña en un hash seguro
    # Recibe la contraseña en texto plano y devuelve el hash
def hash_password(password: str):
    return password_hash.hash(password)

# Función para verificar si una contraseña en texto plano coincide con un hash almacenado
# Retorna True si la contraseña es correcta, False si no lo es
#Se usa para jwt bearer token
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)
