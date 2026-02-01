from database.db import conectarDB

class Productos:
    def __init__(self, id, nombre, imagen, precio, descripcion):
        self.id = id
        self.nombre = nombre
        self.imagen = imagen
        self.precio = precio
        self.descripcion = descripcion

    # Agregar producto
    def agregar(self):
            db = conectarDB()
            cursor = db.cursor()

            cursor.execute("""
                INSERT INTO productos (nombre, imagen, precio, descripcion)
                VALUES (?, ?, ?, ?)
            """, (self.nombre, self.imagen, self.precio, self.descripcion))
            
            # Obtener el id del producto
            self.id = cursor.lastrowid 

            db.commit()
            db.close()

            return self.id
    
    # Asignar la talla y la cantidad
    def asignar_stock(self, id_talla, stock):
        db = conectarDB()
        cursor = db.cursor()

        cursor.execute(""" INSERT INTO variantes_camisas (id_producto, id_talla, stock) VALUES
                            (?, ?, ?) """, (self.id, id_talla, stock))
        
        db.commit()
        db.close()


    @staticmethod
    def obtener_tallas():
        db = conectarDB()
        cursor = db.cursor()
        cursor.execute("SELECT id_talla, talla FROM tallas ORDER BY id_talla")
        tallas = cursor.fetchall()
        db.close()
        return tallas
    
    @staticmethod
    def obtener_producto(id):
        db = conectarDB()
        cursor = db.cursor()

        cursor.execute(""" SELECT p.id_producto, p.nombre, p.imagen, p.precio, p.descripcion, t.talla, vc.stock FROM variantes_camisas vc
                            JOIN productos p ON vc.id_producto = p.id_producto
                            JOIN tallas t ON vc.id_talla = t.id_talla
                            WHERE p.id_producto = ?""", (id,))
        filas = cursor.fetchall()
        db.close()

        if not filas:
            return None

        # Obtener el primer registro
        primer_registro = filas[0]

        variantes = []
        for f in filas:
            variantes.append({
                'talla': f[5],
                'stock': f[6]
            })

        return {
                "id": primer_registro[0],
                "nombre": primer_registro[1],
                "imagen": primer_registro[2],
                "precio": primer_registro[3],
                "descripcion": primer_registro[4],
                "variantes": variantes
            }

    

    @staticmethod
    def listar():
        db = conectarDB()
        cursor = db.cursor()

        cursor.execute("""SELECT * FROM productos""")
        filas = cursor.fetchall()
        db.close()

        productos = []
        for f in filas:
            producto = Productos(
                id = f["id_producto"],
                nombre = f["nombre"],
                imagen = f["imagen"],
                precio = f["precio"],
                descripcion = f["descripcion"]
            )
            productos.append(producto)

        return productos