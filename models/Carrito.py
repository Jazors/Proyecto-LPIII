from database.db import conectarDB

class Carrito:
    
    @staticmethod
    def agregar_producto(id_producto, id_talla, cantidad):
        db = conectarDB()
        cursor = db.cursor()
        # Obtener el stock del producto
        cursor.execute("""
                        SELECT stock FROM variantes_camisas
                        WHERE id_producto = ? AND id_talla = ?
                       """, (id_producto, id_talla))

        stock = cursor.fetchone()

        # Si no hay stock o la cantidad es mayor al stock
        if not stock or cantidad > stock['stock']:
            db.close()
            return False

        # Verificamos si ya está en el carrito
        cursor.execute("""
                        SELECT cantidad FROM carrito
                        WHERE id_producto = ? AND id_talla = ?
                       """, (id_producto, id_talla))

        fila = cursor.fetchone()

        # Si hay una fila retorna la cantidad, sino entonces es 0
        cantidad_actual = fila['cantidad'] if fila else 0

        # Si la cantidad + la cantidad actual es mayor al stock
        if cantidad + cantidad_actual > stock['stock']:
            db.close()
            return False
        
        if fila:
            # Si ya existe una fila en el carrito, sumamos la nueva cantidad a la anterior
            nueva_cantidad = fila['cantidad'] + cantidad
            cursor.execute("""
                            UPDATE carrito SET cantidad = ?
                            WHERE id_producto = ? AND id_talla = ?
                           """, (nueva_cantidad, id_producto, id_talla))
        else:
            # Si no existe, se inserta al carrito
            cursor.execute("INSERT INTO carrito (id_producto, id_talla, cantidad) VALUES (?, ?, ?)", 
                        (id_producto, id_talla, cantidad))
        
        db.commit()
        db.close()
        return True

    @staticmethod
    def obtener_productos():
        db = conectarDB()
        cursor = db.cursor()

        # Obtenemos el producto del carrito
        cursor.execute("""
                        SELECT c.id_carrito, p.nombre, p.imagen, p.precio, t.talla, c.cantidad, (p.precio * c.cantidad) as subtotal
                        FROM carrito c
                        JOIN productos p ON c.id_producto = p.id_producto
                        LEFT JOIN tallas t ON c.id_talla = t.id_talla
                       """)
        productos = cursor.fetchall()
        db.close()
        total = 0
        # Calculamos el total general para mostrarlo en el carrito
        for producto in productos:
            total += producto['subtotal']

        return productos, total


    @staticmethod
    def eliminar_producto(id_carrito):
        db = conectarDB()
        cursor = db.cursor()
        cursor.execute("DELETE FROM carrito WHERE id_carrito = ?", (id_carrito,))
        db.commit()
        db.close()