document.addEventListener("DOMContentLoaded", function () {
    const imageInput = document.getElementById("imageInput");

    imageInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                document.getElementById("preview").src = e.target.result;
                document.getElementById("preview").style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });

    window.classifyImage = function () {
        const fileInput = document.getElementById("imageInput");
        if (fileInput.files.length === 0) {
            alert("Por favor, selecciona una imagen.");
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        fetch("http://localhost:5000/predict", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById("result");
            resultDiv.innerHTML = "<h3>Resultados:</h3>";

            if (data.predictions) {
                data.predictions.forEach(prediction => {
                    resultDiv.innerHTML += `<p>${prediction.class}: ${prediction.confidence}%</p>`;
                });
            } else {
                resultDiv.innerHTML = "<p>Error al procesar la imagen.</p>";
            }
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("result").innerHTML = "<p>Error al clasificar la imagen.</p>";
        });
    };
});
