class Usuario:
    def __init__(self, email, password, id=None, id_rol=None):
        self.id = id
        self.email = email
        self.password = password
        self.id_rol = id_rol