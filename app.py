from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from models.Productos import Productos

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inicio de sesión
@app.route("/login")
def login():
    return render_template('login.html')

#### USUARIO ####

# Página principal
@app.route("/")
def index():
    productos = Productos.listar()
    return render_template('user/index.html', productos = productos)


# Nosotros
@app.route("/nosotros")
def nosotros():
    return render_template('user/nosotros.html')

# Producto
@app.route("/producto/<int:id>")
def producto(id):
    producto = Productos.obtener_producto(id)
    return render_template('user/producto.html', producto = producto)



#### ADMIN ####

# Página principal
@app.route('/admin')
def admin():
    productos = Productos.listar()
    return render_template('admin/index.html', productos = productos)


# Agregar productos
@app.route("/admin/agregar_producto", methods=["GET", "POST"])
def agregar_producto():
    if request.method == "POST":
        # Recibir datos del formulario
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        descripcion = request.form["descripcion"]

        # Capturamos todos los IDs de tallas y todas las cantidades como listas para las diferentes cantidades por cada talla
        ids_tallas = request.form.getlist("id_talla[]")
        cantidades = request.form.getlist("cantidad[]")

        # Revisa que la imagen y el nombre de la imagen no estén vacíos para guardarlo en la carpeta 'uploads'
        archivo = request.files["imagen"]
        if archivo and archivo.filename != "":
            nombre_imagen = secure_filename(archivo.filename)
            archivo.save(os.path.join(UPLOAD_FOLDER, nombre_imagen))

        # Crear objeto
        producto = Productos(None, nombre, nombre_imagen, precio, descripcion)
        # Agregar en la base de datos
        producto.agregar() 

        # Guardar cada talla y cantidad del producto
        for i in range(len(ids_tallas)):
            id_t = ids_tallas[i]
            stock = cantidades[i]

            if stock and int(stock) > 0:
                producto.asignar_stock(id_t, int(stock))

        return redirect(url_for("admin"))

    tallas = Productos.obtener_tallas()
    return render_template("admin/agregar_producto.html", tallas=tallas)


# Actualizar producto
@app.route('/admin/actualizar_producto/<int:id>')
def actualizar_producto(id):
    producto = Productos.obtener_producto(id)
    tallas = Productos.obtener_tallas()
    stock = Productos.obtener_stock_por_producto(id)
    return render_template('admin/actualizar_producto.html', producto = producto, tallas = tallas, stock = stock)



if __name__ == '__main__': 
    app.run(debug=True)