CNN Flower Analyzer

Este proyecto es una aplicación web que permite clasificar imágenes de flores utilizando un modelo de redes neuronales convolucionales (CNN) entrenado con TensorFlow y desplegado con Flask.

📌 Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

Python 3.8+

pip

Git (opcional, pero recomendado)

📥 Instalación

Clona el repositorio:

git clone https://github.com/RuizC0D3/CNN_flower_analyzer.git
cd cnn-flower-analyzer

Instala las dependencias:

pip install -r requirements.txt

🚀 Uso

1️⃣ Iniciar el servidor Flask

Ejecuta el siguiente comando:

python app.py

El servidor se ejecutará en http://127.0.0.1:5000/.

2️⃣ Abrir la aplicación en el navegador

Abre http://127.0.0.1:5000/ en tu navegador para ver la interfaz web.

3️⃣ Subir una imagen

Carga una imagen de una flor y el modelo la clasificará, mostrando el resultado en la pantalla.

📂 Estructura del proyecto

cnn-flower-analyzer/
│── model/                 # Carpeta con el modelo preentrenado
│   ├── flowers-model.keras
│── uploads/               # Carpeta donde se almacenan las imágenes subidas
│── static/                # Archivos estáticos
│   ├── styles.css         # Estilos de la web
│   ├── script.js          # Funcionalidad en JavaScript
│── templates/             # Archivos HTML
│   ├── index.html         # Página principal
│── app.py                 # Código principal de Flask
│── requirements.txt       # Dependencias del proyecto
│── README.md              # Documentación

🛠 Posibles errores y soluciones

🔴 Error al clasificar la imagen

Asegúrate de que el modelo flowers-model.keras está en la carpeta model/.

Revisa que la imagen subida tiene formato válido (.jpg, .png, .jpeg).

🔴 CORS policy blocked request

Si la aplicación web no puede comunicarse con Flask, instala flask-cors:

pip install flask-cors

Y en app.py, agrega:

from flask_cors import CORS
CORS(app)

🔴 El resultado no cambia al subir otra imagen

Intenta limpiar la caché de la página (Ctrl + Shift + R) o revisa script.js para asegurarte de que el resultado se actualiza correctamente.

📜 Licencia

Este proyecto está bajo la licencia MIT.

¡Disfruta usando el CNN Flower Analyzer! 🌸🚀