from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Inicializar la app Flask
app = Flask(__name__)

# Cargar el modelo entrenado
MODEL_PATH = os.path.join("models", "flowers-model.keras")
model = tf.keras.models.load_model(MODEL_PATH)

# Clases del modelo
class_names = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']  # Ajusta esto según tu dataset

# Preprocesamiento de la imagen
def preprocess_image(image_path):
    img = Image.open(image_path).resize((180, 180))
    img = np.array(img) / 255.0  # Normalizar
    img = np.expand_dims(img, axis=0)  # Agregar batch dimension
    return img

# Ruta para predecir la imagen
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No se envió ninguna imagen'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400
    
    # Guardar imagen temporalmente
    image_path = "temp.jpg"
    file.save(image_path)
    
    # Procesar la imagen y hacer la predicción
    img = preprocess_image(image_path)
    predictions = model.predict(img)
    os.remove(image_path)  # Eliminar la imagen temporal
    
    predicted_class = class_names[np.argmax(predictions)]
    confidence = float(np.max(predictions))
    
    return jsonify({'class': predicted_class, 'confidence': confidence})

if __name__ == '__main__':
    app.run(debug=True)
