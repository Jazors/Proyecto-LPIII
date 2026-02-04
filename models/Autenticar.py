from database.db import conectarDB
import hashlib

class Autenticar:
    def __init__(self, email, password, id=None):
        self.id = id
        self.email = email
        self.password = password



    #@staticmethod
    #def verificar_email(email):



    #@staticmethod
    #def verificar_password(email, password):