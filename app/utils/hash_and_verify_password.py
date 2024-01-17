import bcrypt
# Función para hashear la contraseña
def hash_password(password: str) -> str:
    try:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    except Exception as e:
        print(f"Error al hashear la contraseña: {e}")

# Función para verificar la contraseña hasheada
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Error al verificar la contraseña: {e}")