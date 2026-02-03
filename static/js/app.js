document.getElementById('imagen').addEventListener('change', function(event) {
  
  // Verifica si existe un archivo seleccionado, si existe, extrae el nombre, si no, usa un texto por defecto.
  const nombreArchivo = event.target.files[0] ? event.target.files[0].name : 'Ningún archivo seleccionado';

  // Actualiza el contenido del id 'nombre_imagen' HTML con el nombre obtenido para dar feedback al usuario.
  document.getElementById('nombre_imagen').textContent = nombreArchivo;
});