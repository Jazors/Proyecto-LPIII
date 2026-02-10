const modal = document.getElementById("modalCompra");
const btnAbrir = document.querySelector(".btn-secundario");
const btnCerrar = document.querySelector(".cerrar-modal");

// Abrir modal
btnAbrir.onclick = function(e) {
    e.preventDefault();
    modal.style.display = "flex";
}

// Cerrar al hacer clic en la X
btnCerrar.onclick = function() {
    modal.style.display = "none";
}

// Cerrar si hacen clic fuera de la caja blanca
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}