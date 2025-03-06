console.log("✅ script.js cargado correctamente");

document.getElementById('imageInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('preview').src = e.target.result;
            document.getElementById('preview').style.display = 'block';
        }
        reader.readAsDataURL(file);
    }
});

function classifyImage() {
    const fileInput = document.getElementById('imageInput');
    if (fileInput.files.length === 0) {
        alert('Por favor, selecciona una imagen.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch("http://127.0.0.1:5000/predict", {

        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = 'Resultado: ' + data.class + ' (Confianza: ' + (data.confidence * 100).toFixed(2) + '%)';
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error al clasificar la imagen.';
    });
}