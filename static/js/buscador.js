document.addEventListener('DOMContentLoaded', () => {
    const input = document.querySelector('.buscador');
    const tabla = document.querySelector('.tabla');

    // Obtener filas de los datos en la tabla
    const filas = tabla.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

    // Columna de nombre
    const columnaNombre = 0;

    input.addEventListener('keyup', () => {

        // Convertir a minúsculas el texto ingresado en el input
        const filtro = input.value.toLowerCase();

        for (let i=0; i<filas.length; i++) {

            // Celdas de la tabla
            const celdas = filas[i].getElementsByTagName('td');
            
            // Si hay celdas del texto ingresado en el input
            if (celdas.length > 0) {

                // Convertir a minúscula el texto que proviene de la tabla
                const textoCeldas = celdas[columnaNombre].textContent.toLowerCase();

                // Revisa si coincide el texto de la tabla con el ingresado por el input
                if (textoCeldas.includes(filtro)) {
                    // Si coincide se muestra en la tabla
                    filas[i].style.display = '';
                } else {
                    // Si no coincide lo oculta de la tabla
                    filas[i].style.display = 'none';
                }
            }
        }

    });

});