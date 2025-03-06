from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
import os
from werkzeug.utils import secure_filename
from PIL import Image

# Inicializar Flask
app = Flask(__name__)

# Configuración de rutas y modelo
MODEL_PATH = "model/flowers-model.keras"
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Crear carpeta de uploads si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cargar modelo
model = tf.keras.models.load_model(MODEL_PATH)

# Clases de flores (asegúrate de que coincidan con las de tu dataset)
class_names = ["daisy", "dandelion", "roses", "sunflowers", "tulips"]

# Función para verificar formato de imagen
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta principal (Carga la página web)
@app.route("/")
def home():
    return render_template("index.html")

# Ruta para subir imagen y clasificarla
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No se subió ninguna imagen"})
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No se seleccionó ningún archivo"})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Preprocesar imagen
        img = Image.open(filepath).resize((180, 180))
        img = np.array(img) / 255.0  # Normalizar
        img = np.expand_dims(img, axis=0)  # Agregar batch dimension
        
        # Realizar predicción
        predictions = model.predict(img)
        predicted_class = class_names[np.argmax(predictions)]
        confidence = float(np.max(predictions))
        
        return jsonify({"class": predicted_class, "confidence": confidence})
    
    return jsonify({"error": "Formato de archivo no permitido"})

if __name__ == "__main__":
    app.run(debug=True)