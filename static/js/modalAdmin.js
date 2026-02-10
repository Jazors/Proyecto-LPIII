function abrirModal(id) {
    document.getElementById('modal-' + id).style.display = 'flex';
}

function cerrarModal(id) {
    document.getElementById('modal-' + id).style.display = 'none';
}

// Cerrar si hace clic fuera del contenido
window.onclick = function(event) {
    if (event.target.className === 'modal') {
        event.target.style.display = "none";
    }
}