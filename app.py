from flask import Flask, flash, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from models.Productos import Productos
from models.Autenticar import Autenticar

app = Flask(__name__)
app.secret_key = '454ghgghfg8h9fghjnrjtr'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inicio de sesión
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('Rellene todos los campos', 'danger')
            return redirect(request.url)
        
        autenticado = Autenticar.verificar_email(email)
        if not autenticado:
            flash('El email no existe', 'danger')
            return redirect(request.url)
        autenticado = Autenticar.verificar_password(email, password)
        if not autenticado:
            flash('Contraseña incorrecta', 'danger')
            return redirect(request.url)
        
        session['user'] = email
        return redirect(url_for('admin'))

    return render_template('login.html')

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

#### CLIENTE ####

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

# Agregar al carrito
@app.route('/agregar_carrito', methods=["GET", "POST"])
def agregar_al_carrito():
    if request.method=='POST':
        id_producto = request.form['id_producto']
        talla = request.form['talla']
        stock = request.form['cantidad']
        
        return redirect('/')

@app.route('/carrito')
def carrito():
    return render_template('user/carrito_compras.html')


#### ADMIN ####

# Página principal
@app.route('/admin')
def admin():
    productos = Productos.listar()
    tallas = Productos.obtener_tallas()
    return render_template('admin/index.html', productos = productos, tallas = tallas)


# Agregar productos
@app.route("/admin/agregar_producto", methods=["GET", "POST"])
def agregar_producto():
    if request.method == "POST":

        # Recibir datos del formulario
        nombre = request.form["nombre"]
        archivo = request.files["imagen"]
        precio = request.form["precio"]
        descripcion = request.form["descripcion"]
        codigo = request.form["codigo"]

        # Capturamos todos los IDs de tallas y todas las cantidades como listas (esto es porque son diferentes cantidades por cada talla)
        ids_tallas = request.form.getlist("id_talla[]")
        cantidades = request.form.getlist("cantidad[]")

        # Validamos que no estén vacíos todos los campos del formulario
        if not nombre or not precio or not descripcion or not codigo or not archivo:
            flash('Rellene todos los campos', 'danger')
            return redirect(request.url)

        # Revisa que la imagen y el nombre de la imagen no estén vacíos para guardarlo en la carpeta 'uploads'
        if archivo and archivo.filename != "":
            nombre_imagen = secure_filename(archivo.filename)
            archivo.save(os.path.join(UPLOAD_FOLDER, nombre_imagen))

        # Crear objeto
        producto = Productos(None, nombre, nombre_imagen, precio, descripcion, codigo)
        # Agregar en la base de datos
        producto.agregar() 

        # Relacionar tallas con sus cantidades y registrar solo aquellas con stock disponible
        for id_t, stock in zip(ids_tallas, cantidades):

            # Si la cantidad de la talla es mayor o igual a 0 lo guarda (también lo convierte en entero)
            if stock and int(stock) >= 0:
                producto.asignar_stock(id_t, int(stock))

        # Redirecciona al index del admin
        flash('Se agregó correctamente', 'success')
        return redirect(url_for("admin"))
        

    tallas = Productos.obtener_tallas()
    return render_template("admin/agregar_producto.html", tallas=tallas)


# Actualizar producto
@app.route('/admin/actualizar_producto/<int:id>', methods=['GET', 'POST'])
def actualizar_producto(id):
    if request.method == "POST":
        producto = Productos.obtener_producto(id)

        # Recibir datos del formulario
        nombre = request.form["nombre"]
        archivo = request.files["imagen"]
        precio = request.form["precio"]
        descripcion = request.form["descripcion"]
        codigo = request.form["codigo"]

        # Capturamos todos los IDs de tallas y todas las cantidades como listas (esto es porque son diferentes cantidades por cada talla)
        ids_tallas = request.form.getlist("id_talla[]")
        cantidades = request.form.getlist("cantidad[]")

        # Validamos que no estén vacíos todos los campos del formulario
        if not nombre or not precio or not descripcion or not codigo:
            flash('Rellene todos los campos', 'danger')
            return redirect(request.url)
    
        # Revisa que la imagen y el nombre de la imagen no estén vacíos para guardarlo en la carpeta 'uploads'
        nombre_imagen = producto['imagen']
        if archivo and archivo.filename != "":
            nombre_imagen = secure_filename(archivo.filename)
            archivo.save(os.path.join(UPLOAD_FOLDER, nombre_imagen))

        producto_act = Productos(None, nombre, nombre_imagen, precio, descripcion, codigo)
        producto_act.actualizar(id)

        # Relacionar tallas con sus cantidades y registrar solo aquellas con stock disponible
        for id_t, stock in zip(ids_tallas, cantidades):

            # Si la cantidad de la talla es mayor o igual a 0 lo guarda (también lo convierte en entero)
            if stock and int(stock) >= 0:
                Productos.actualizar_stock(id, id_t, int(stock))


        flash('Actualizado correctamente', 'success')
        return redirect(url_for('admin'))

    producto = Productos.obtener_producto(id)
    tallas = Productos.obtener_tallas()
    stock = Productos.obtener_stock_por_producto(id)
    return render_template('admin/actualizar_producto.html', producto = producto, tallas = tallas, stock = stock)


# Eliminar producto
@app.route('/admin/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):

    # Obtenemos la info del producto (mientras aún exista)
    producto = Productos.obtener_producto(id)
    
    # Verificamos que exista el producto con ese id
    if not producto:
        flash('El producto no existe', 'danger')
        return redirect(url_for('admin'))

    # Borramos la imagen (si existe)
    if producto['imagen']:
        ruta_imagen = os.path.join(app.config['UPLOAD_FOLDER'], producto['imagen'])
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

    # Borramos de la base de datos
    Productos.eliminar(id)
    
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('admin'))

# Ejecuta el servidor en modo desarrollador
if __name__ == '__main__': 
    app.run(debug=True)