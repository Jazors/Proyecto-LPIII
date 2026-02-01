from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from models.Producto import Producto

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
    productos = Producto.listar()
    return render_template('user/index.html', productos = productos)


# Nosotros
@app.route("/nosotros")
def nosotros():
    return render_template('user/nosotros.html')

# Producto
@app.route("/producto/<int:id>")
def producto(id):
    producto = Producto.obtener_producto(id)
    return render_template('user/producto.html', producto = producto)



#### ADMIN ####
# Agregar producto
@app.route("/agregar_producto", methods=["GET", "POST"])
def agregar_producto():

    if request.method == "POST":
        # Recibir atributos del formulario
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        descripcion = request.form["descripcion"]
        id_talla = request.form["talla"]
        stock = request.form["cantidad"]

        archivo = request.files["imagen"]
        nombre_imagen = None

        # Revisa que la imagen y el nombre de la imagen no estén vacíos para guardarlo en la carpeta 'uploads'
        if archivo and archivo.filename != "":
            nombre_imagen = secure_filename(archivo.filename)
            archivo.save(os.path.join(UPLOAD_FOLDER, nombre_imagen))

        # Crear objeto
        producto = Producto(None, nombre, nombre_imagen, precio, descripcion)

        # Insertar en la BD
        producto.agregar()
        producto.asignar_stock(id_talla, stock)

        # Redireccionar al index
        return redirect(url_for("index"))

    tallas = Producto.obtener_tallas()
    return render_template("admin/agregar_producto.html", tallas = tallas)




if __name__ == '__main__': 
    app.run(debug=True)