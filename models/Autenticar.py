from database.db import conectarDB
import hashlib

class Autenticar:

    @staticmethod
    def verificar_email(email):
        db = conectarDB()
        cursor = db.cursor()

        cursor.execute("""
                       SELECT email FROM usuarios
                       WHERE email = ?
                       """,(email,))
        resultado = cursor.fetchone()

        db.close()

        if resultado:
            return True
        else:
            return False 



    @staticmethod
    def verificar_password(email, password):
        db = conectarDB()
        cursor = db.cursor()

        cursor.execute("""
                        SELECT password FROM usuarios
                        WHERE email = ?                                            
                       """,(email,))
        resultado = cursor.fetchone()
        db.close()

        hashed_password = resultado[0]

        if hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed_password:
            return True
        else:
            return False