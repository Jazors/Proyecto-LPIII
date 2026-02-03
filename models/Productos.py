from database.db import conectarDB

class Productos:
    def __init__(self, id, nombre, imagen, precio, descripcion, codigo):
        self.id = id
        self.nombre = nombre
        self.imagen = imagen
        self.precio = precio
        self.descripcion = descripcion
        self.codigo = codigo

    # Agregar producto
    def agregar(self):
            db = conectarDB()
            cursor = db.cursor()

            cursor.execute("""
                            INSERT INTO productos (nombre, imagen, precio, descripcion, codigo)
                            VALUES (?, ?, ?, ?, ?)
                            """, (self.nombre, self.imagen, self.precio, self.descripcion, self.codigo))
            
            # Obtener el id del producto recién agregado
            self.id = cursor.lastrowid 

            db.commit()
            db.close()

            return self.id
    
    # Asignar la talla y la cantidad
    def asignar_stock(self, id_talla, stock):
        db = conectarDB()
        cursor = db.cursor()

        cursor.execute(""" REPLACE INTO variantes_camisas (id_producto, id_talla, stock) VALUES
                            (?, ?, ?) """, (self.id, id_talla, stock))
        
        db.commit()
        db.close()

    # Eliminar producto
    @staticmethod
    # def eliminar(id):

    @staticmethod
    def obtener_tallas():
        db = conectarDB()
        cursor = db.cursor()
        cursor.execute("SELECT id_talla, talla FROM tallas")
        tallas = cursor.fetchall()
        db.close()
        return tallas

    
    @staticmethod
    def obtener_stock_por_producto(id):
        db = conectarDB()
        cursor = db.cursor()
        cursor.execute("""SELECT t.talla, vc.stock FROM variantes_camisas vc
                            LEFT JOIN tallas t ON vc.id_talla = t.id_talla
                            WHERE vc.id_producto = ?
                        """, (id,))
        stock_detalle = cursor.fetchall()
        db.close()
        return stock_detalle
    
    @staticmethod
    def obtener_producto(id):
        db = conectarDB()
        cursor = db.cursor()

        cursor.execute(""" SELECT p.id_producto, p.nombre, p.imagen, p.precio, p.descripcion, p.codigo, t.talla, vc.stock FROM variantes_camisas vc
                            JOIN productos p ON vc.id_producto = p.id_producto
                            JOIN tallas t ON vc.id_talla = t.id_talla
                            WHERE p.id_producto = ?
                       """, (id,))
        filas = cursor.fetchall()
        db.close()

        if not filas:
            return None

        # Obtenemos los datos de la primera fila de la consulta
        primer_registro = filas[0]

        # Retorna un diccionario con los datos de la consulta
        return {
                "id": primer_registro[0],
                "nombre": primer_registro[1],
                "imagen": primer_registro[2],
                "precio": primer_registro[3],
                "descripcion": primer_registro[4],
                "codigo": primer_registro[5],
                "variantes": [{"talla": f[6], "stock": f[7]} for f in filas]
            }


    @staticmethod
    def listar():
        db = conectarDB()
        cursor = db.cursor()

        cursor.execute("""SELECT * FROM productos""")
        filas = cursor.fetchall()
        db.close()

        # Lista de productos y sus variantes
        productos = []
        for f in filas:
            producto = Productos(
                id = f["id_producto"],
                nombre = f["nombre"],
                imagen = f["imagen"],
                precio = f["precio"],
                descripcion = f["descripcion"],
                codigo = f["codigo"]
            )

            producto.variantes = Productos.obtener_stock_por_producto(producto.id)
            productos.append(producto)

        return productos