document.getElementById('imagen').addEventListener('change', function(event) {
  const nombreArchivo = event.target.files[0] ? event.target.files[0].name : 'Ningún archivo seleccionado';
  document.getElementById('nombre_imagen').textContent = nombreArchivo;
});