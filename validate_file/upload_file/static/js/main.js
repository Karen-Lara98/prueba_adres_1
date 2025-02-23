document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var form = e.target;
    var fileInput = form.querySelector('input[type="file"]');
    if(fileInput.files.length === 0) return;
    
    var formData = new FormData(form);
    var progressContainer = document.getElementById('progressContainer');
    var progressBar = document.getElementById('progressBar');
    var progressText = document.getElementById('progressText');
    var resultContainer = document.getElementById('resultContainer');
    
    progressContainer.style.display = 'block';
    progressBar.classList.remove('progress-error', 'progress-success'); // Reset de color
    progressBar.style.width = '0%';
    progressText.innerText = '0%';

    var xhr = new XMLHttpRequest();
    xhr.open('POST', form.action);

    // Establecemos la cabecera para identificar la petición como AJAX
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    // Simulación de carga progresiva
    let simulatedProgress = 0;
    var fakeProgress = setInterval(function() {
        if (simulatedProgress < 90) {  // Solo avanza hasta 90% para dejar que el real lo complete
            simulatedProgress += 5;
            progressBar.style.width = simulatedProgress + '%';
            progressText.innerText = simulatedProgress + '%';
        } else {
            clearInterval(fakeProgress); // Detenemos la simulación en 90%
        }
    }, 200); // Cada 200ms incrementa 5%

    xhr.upload.addEventListener('progress', function(e) {
        if(e.lengthComputable) {
            var percent = Math.round((e.loaded / e.total) * 100);
            if (percent > simulatedProgress) { // Solo actualiza si el real es mayor que el simulado
                progressBar.style.width = percent + '%';
                progressText.innerText = percent + '%';
            }
        }
    });

    xhr.onload = function() {
        clearInterval(fakeProgress); // Detener la simulación al finalizar

        if(xhr.status === 200) {
            try {
                var response = JSON.parse(xhr.responseText);
                resultContainer.innerHTML = '<pre>' + response.result + '</pre>';
                progressText.innerText = 'Carga completada';
                progressBar.classList.add('progress-success'); // Color verde para éxito
            } catch(err) {
                resultContainer.innerHTML = '<pre style="color:red;">Error inesperado en la respuesta del servidor.</pre>';
            }
        } else {
            try {
                var response = JSON.parse(xhr.responseText);
                resultContainer.innerHTML = '<pre style="color:red;">' + response.result + '</pre>';
            } catch(err) {
                resultContainer.innerHTML = '<pre style="color:red;">Error: No se pudo procesar la respuesta del servidor.</pre>';
            }
            progressText.innerText = 'Error en la carga';
            progressBar.classList.add('progress-error'); // Color rojo en caso de error
        }
    };

    xhr.onerror = function() {
        clearInterval(fakeProgress);
        resultContainer.innerHTML = '<pre style="color:red;">Error: No se pudo conectar con el servidor.</pre>';
        progressBar.classList.add('progress-error'); // Color rojo en error de conexión
    };

    xhr.send(formData);
});    