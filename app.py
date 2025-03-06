from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

# Inicializar Flask
app = Flask(__name__, static_folder="static")
CORS(app)

# Cargar el modelo de clasificación de flores
try:
    model = tf.keras.models.load_model("model/flowers-model.keras")
    print("✅ Modelo cargado correctamente")
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")
    model = None  # Evita que Flask intente predecir si no hay modelo

# Clases de flores del dataset Oxford 102
class_names = [
    "pink primrose", "hard-leaved pocket orchid", "canterbury bells", "sweet pea", "english marigold",
    "tiger lily", "moon orchid", "bird of paradise", "monkshood", "globe thistle", "snapdragon", "colts foot",
    "king protea", "spear thistle", "yellow iris", "globe-flower", "purple coneflower", "peruvian lily",
    "balloon flower", "giant white arum lily", "fire lily", "pincushion flower", "fritillary", "red ginger",
    "grape hyacinth", "corn poppy", "prince of wales feathers", "stemless gentian", "artichoke", "sweet william",
    "carnation", "garden phlox", "love in the mist", "mexican aster", "alpine sea holly", "ruby-lipped cattleya",
    "cape flower", "great masterwort", "siam tulip", "lenten rose", "barbeton daisy", "daffodil", "sword lily",
    "poinsettia", "bolero deep blue", "wallflower", "marigold", "buttercup", "oxeye daisy", "common dandelion",
    "petunia", "wild pansy", "primula", "sunflower", "pelargonium", "bishop of llandaff", "gaura", "geranium",
    "orange dahlia", "pink-yellow dahlia", "cautleya spicata", "japanese anemone", "black-eyed susan", "silverbush",
    "californian poppy", "osteospermum", "spring crocus", "bearded iris", "windflower", "tree poppy",
    "gazania", "azalea", "water lily", "rose", "thorn apple", "morning glory", "passion flower", "lotus",
    "toad lily", "anthurium", "frangipani", "clematis", "hibiscus", "columbine", "desert rose", "tree mallow",
    "magnolia", "cyclamen", "watercress", "canna lily", "hippeastrum", "bee balm", "ball moss", "foxglove",
    "bougainvillea", "camellia", "mallow", "mexican petunia", "bromelia", "blanket flower", "trumpet creeper",
    "blackberry lily", "common tulip", "wild rose"
]

# Función para preprocesar la imagen antes de ingresarla al modelo
def preprocess_image(image):
    image = image.convert("RGB")  # Convierte a RGB (3 canales)
    image = image.resize((180, 180))  # Redimensiona a 180x180 píxeles
    image = np.array(image) / 255.0  # Normaliza a valores entre 0 y 1
    image = np.expand_dims(image, axis=0)  # Expande dimensiones para coincidir con el input del modelo
    return image

# Ruta para servir la página principal
@app.route("/")
def serve_index():
    return send_from_directory("templates", "index.html")

# Ruta para predecir la clase de la imagen
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No se encontró ninguna imagen"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No se seleccionó ninguna imagen"}), 400

    try:
        print("📸 Imagen recibida:", file.filename)

        image = Image.open(io.BytesIO(file.read()))
        image = preprocess_image(image)

        print("✅ Imagen preprocesada correctamente")

        if model is None:
            print("❌ ERROR: El modelo no se cargó correctamente")
            return jsonify({"error": "El modelo no está cargado"}), 500

        predictions = model.predict(image)
        print("📊 Predicciones:", predictions)

        # Obtener las tres mejores predicciones con sus probabilidades y formatear a 2 decimales
        top_indices = np.argsort(predictions[0])[-3:][::-1]
        results = [{"class": class_names[i], "confidence": round(float(predictions[0][i] * 100), 2)} for i in top_indices]

        print("📋 Resultados:", results)
        return jsonify({"predictions": results})

    except Exception as e:
        print(f"❌ ERROR en la predicción: {e}")  # Imprimir el error en la consola
        return jsonify({"error": str(e)}), 500

# Ejecutar Flask en modo debug
if __name__ == "__main__":
    app.run(debug=True)
