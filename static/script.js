console.log("✅ script.js cargado correctamente");

// Esperar a que el DOM esté completamente cargado antes de asignar eventos
document.addEventListener("DOMContentLoaded", function () {
    const imageInput = document.getElementById("imageInput");
    const preview = document.getElementById("preview");
    const resultText = document.getElementById("result");
    const classifyBtn = document.getElementById("classifyBtn");

    // Función para previsualizar la imagen
    imageInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = "block";
                resultText.innerText = ""; // Resetear el resultado al cambiar la imagen
            };
            reader.readAsDataURL(file);
        }
    });

    // Función para enviar la imagen al backend y obtener la predicción
    classifyBtn.addEventListener("click", function () {
        if (!imageInput.files.length) {
            alert("⚠️ Por favor, selecciona una imagen.");
            return;
        }

        const formData = new FormData();
        formData.append("file", imageInput.files[0]);

        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    resultText.innerText = "❌ Error: " + data.error;
                } else {
                    resultText.innerText = `🌼 Resultado: ${data.class} (Confianza: ${(data.confidence * 100).toFixed(2)}%)`;
                }
            })
            .catch((error) => {
                console.error("🚨 Error al procesar la imagen:", error);
                resultText.innerText = "❌ Error al clasificar la imagen.";
            });
    });
});
