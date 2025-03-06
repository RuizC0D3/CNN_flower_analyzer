from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import os
from werkzeug.utils import secure_filename
from PIL import Image

# Inicializar Flask
app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})  # Permitir CORS en /predict

# Configuración de rutas y modelo
MODEL_PATH = "model/flowers-model.keras"
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cargar modelo
model = tf.keras.models.load_model(MODEL_PATH)

# Clases de flores
class_names = ["daisy", "dandelion", "roses", "sunflowers", "tulips"]

# Función para verificar formato de imagen
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

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
        img = Image.open(filepath).convert("RGB").resize((180, 180))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)
        
        # Realizar predicción
        predictions = model.predict(img)
        predicted_class = class_names[np.argmax(predictions)]
        confidence = float(np.max(predictions))
        
        return jsonify({"class": predicted_class, "confidence": confidence})
    
    return jsonify({"error": "Formato de archivo no permitido"})

if __name__ == "__main__":
    app.run(debug=True)
