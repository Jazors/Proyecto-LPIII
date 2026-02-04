# from database.db import conectarDB
# import hashlib

# # Crear un hash SHA-256 de una contraseña
# email = 'frontendstore@gmail.com'
# password = '123456'
# hash_object = hashlib.sha256(password.encode('utf-8'))
# hashed_password = hash_object.hexdigest()

# print(f"Hash de la contraseña: {hashed_password}")
# db = conectarDB()
# cursor = db.cursor()
# cursor.execute("""INSERT INTO usuarios (email, password)
#                     VALUES (?, ?)
#                """, (email, hashed_password))

# db.commit()
# db.close()
