from database.db import conectarDB

class Ventas:
    @staticmethod
    def registrar_cliente(datos_cliente):
        db = conectarDB()
        cursor = db.cursor()
    
        # Registrar al Cliente y obtener su ID
        cursor.execute("""
                        INSERT INTO clientes (nombre, telefono, direccion) 
                        VALUES (?, ?, ?)
                       """, 
                       (datos_cliente['nombre'], datos_cliente['telefono'], datos_cliente['direccion']))
        
        id_cliente = cursor.lastrowid
        db.commit()
        db.close()

        return id_cliente

    @staticmethod
    def crear_venta(id_cliente):
        db = conectarDB()
        cursor = db.cursor()

        # Crear la Venta vinculada al cliente
        cursor.execute("""
                        INSERT INTO ventas (id_cliente, fecha) 
                        VALUES (?, datetime('now'))
                       """, (id_cliente,))
        
        
        id_venta = cursor.lastrowid

        db.commit()
        db.close()
        return id_venta
    
    @staticmethod
    def procesar_productos(id_venta):
        db = conectarDB()
        cursor = db.cursor()

        try:
            cursor.execute("SELECT id_producto, id_talla, cantidad FROM carrito")
            productos_carrito = cursor.fetchall()
            
            # Procesar cada producto del carrito
            for producto in productos_carrito:
                id_producto, id_talla, cantidad = producto

                # Actualizar Stock de variantes_camisas
                cursor.execute("""
                                UPDATE variantes_camisas 
                                SET stock = stock - ? 
                                WHERE id_producto = ? AND id_talla = ? AND stock >= ?
                               """, (cantidad, id_producto, id_talla, cantidad))

                # Si no hay nada es porque no hay stock
                if cursor.rowcount == 0:
                    raise Exception("Stock insuficiente")
                # Guardar en la tabla detalles_venta
                cursor.execute("""
                                INSERT INTO detalles_venta (id_venta, id_producto, id_talla, cantidad)
                                VALUES (?, ?, ?, ?)
                               """, (id_venta, id_producto, id_talla, cantidad))

            # Calcular el total de la venta
            cursor.execute("""
                            UPDATE ventas
                            SET total = (
                                SELECT SUM(dv.cantidad * p.precio)
                                FROM detalles_venta dv
                                JOIN productos p ON dv.id_producto = p.id_producto
                                WHERE dv.id_venta = ?
                            )
                            WHERE id_venta = ?
                           """, (id_venta, id_venta))

            # Vaciar el carrito para la próxima venta
            cursor.execute("DELETE FROM carrito")
            db.commit()
            return True, "Compra realizada con éxito"
        except:
            # Si algo falla, el rollback deshace todo (incluyendo el stock restado antes del error)
            db.rollback()
            return False, "Error"
            
        finally:
            db.close()

    # Detalles de la venta (cliente)
    @staticmethod
    def detalles_venta(id_venta):
        db = conectarDB()
        cursor = db.cursor()
        
        # Obtenemos los datos del cliente y la venta
        cursor.execute("""
                        SELECT v.id_venta, v.fecha, v.total, c.nombre, c.direccion 
                        FROM ventas v 
                        JOIN clientes c ON v.id_cliente = c.id_cliente 
                        WHERE v.id_venta = ?
                       """, (id_venta,))
        venta = cursor.fetchone()
        
        # Obtenemos los productos
        cursor.execute("""
                        SELECT p.nombre, t.talla, dv.cantidad, p.precio, (dv.cantidad * p.precio) as subtotal
                        FROM detalles_venta dv
                        JOIN productos p ON dv.id_producto = p.id_producto
                        JOIN tallas t ON dv.id_talla = t.id_talla
                        WHERE dv.id_venta = ?
                       """, (id_venta,))
        productos = cursor.fetchall()
        
        db.close()
        return venta, productos # Tupla
    

    # Obtener todos los pedidos (admin)
    @staticmethod
    def lista_pedidos():
        db = conectarDB()
        cursor = db.cursor()

        cursor.execute("""
                        SELECT 
                            p.nombre AS producto, p.precio, p.codigo,
                            t.talla, 
                            v.total, 
                            c.nombre AS cliente, c.telefono, c.direccion,
                            dv.cantidad,
                            (dv.cantidad * p.precio) AS subtotal
                        FROM detalles_venta dv
                        JOIN productos p ON dv.id_producto = p.id_producto
                        JOIN tallas t ON dv.id_talla = t.id_talla
                        JOIN ventas v ON dv.id_venta = v.id_venta
                        JOIN clientes c ON v.id_cliente = c.id_cliente
                        ORDER BY
                            id_detalles_venta
                        DESC
                       """)
        filas = cursor.fetchall()
        db.close()

        return filas