from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import base64
from io import BytesIO
from PIL import Image
#import Image
import traceback
from functools import wraps
import os
from flask_cors import CORS
import stat
from datetime import datetime
import json

from download_model import download_model

'''
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
'''

app = Flask(__name__)

CORS(app, resources={
    r"/predict": {
        "origins": "*",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "X-API-Key"]
    },
    r"/predictUsg": {
        "origins": "*",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "X-API-Key"]
    }
})

API_KEY = os.getenv('API_KEY')  # klucz przechowywany w zmiennych środowiskowych
print("API_KEY=", API_KEY)

MODEL_RTG_PATH = os.getenv('MODEL_RTG_PATH', 'pneumonia_classification_model_bal.keras')
MODEL_USG_PATH = os.getenv('MODEL_USG_PATH', 'breast_usg_model.keras')


def list_models():
    try:
        models_dir = '/app/models'
        files_info = []

        print("\n=== Starting directory listing of /app/models ===")

        for root, dirs, files in os.walk(models_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_stat = os.stat(file_path)
                file_info = {
                    'name': file_name,
                    'path': file_path,
                    'size': file_stat.st_size,
                    'permissions': stat.filemode(file_stat.st_mode),
                    'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                    'uid': file_stat.st_uid,
                    'gid': file_stat.st_gid
                }
                files_info.append(file_info)

                # Log each file details
                print(f"\nFile: {file_name}")
                print(json.dumps(file_info, indent=2))

        print("\n=== Directory listing complete ===")
        return files_info

    except Exception as e:
        print(f"Error listing directory: {str(e)}")
        return []

def load_model_from_volume(model_path):
    try:
        print("\n=== Checking model directory contents ===")
        files = list_models()
        print(f"Found {len(files)} files in models directory")
        print(f"Wczytywanie modelu z {model_path}")
        if not os.path.exists(model_path):
            #raise FileNotFoundError(f"Model nie znaleziony w {model_path}")
            print(f"Model nie znaleziony w {model_path}")

        modelml = tf.keras.models.load_model(model_path)
        print("Model wczytany pomyślnie")
        return modelml

    except Exception as e:
        print(f"Błąd podczas wczytywania modelu: {str(e)}")
        #raise


#pobranie modeli z Azure Blob Storage
download_model()

# Wczytanie modelu przy starcie
model = load_model_from_volume(MODEL_RTG_PATH)
modelUsg = load_model_from_volume(MODEL_USG_PATH)

# Ładowanie modelu (plik .h5 lub .keras)
#model = tf.keras.models.load_model("pneumonia_classification_model_bal.keras")
#modelUsg = tf.keras.models.load_model("breast_usg_model.keras")

# Mapowanie indeksów na etykiety klas – kolejność musi odpowiadać kolejności użytej podczas trenowania modelu
class_names = ['benign', 'malignant', 'normal']

'''
limiter = Limiter(
    app,
    #key_func=get_remote_address,
    default_limits=["1000 per day", "100 per minute"]
)
'''
'''
Talisman(app,
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'"
    }
)
'''

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == API_KEY:
            return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    return decorated

@app.route('/predict', methods=['POST'])
@require_api_key
def predict():

    # Oczekujemy danych wejściowych jako JSON z kluczem "image_base64"
    print('predict - enter')

    #print('request files: ', request.files.keys())
    #print('request data: ', request.get_data())

    #if 'file' not in request.files:
        #return jsonify({"error": "Brak pliku w żądaniu. Upewnij się, że wysyłasz plik z kluczem 'file'."}), 400

    try:

        #file = request.files['file']
        #image_b64 = request.get_data(as_text=True)
        #image_bytes = base64.b64decode(image_b64)
        image_bytes = request.get_data()
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        # tylko dla modelu GRAYSCALE
        #image = image.convert('L')  # 'L' oznacza skalę szarości

        image = image.resize((150, 150))
        img_array = img_to_array(image)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Predykcja
        prediction = model.predict(img_array)[0][0]
        label = "Pneumonia" if prediction > 0.5 else "Normal"
        print(jsonify({"prediction": float(prediction), "label": label}))
        return jsonify({"prediction": float(prediction), "label": label})

    except Exception as e:
        error_details = {
            "error": "Internal Server Error",
            "message": str(e),
            "trace": traceback.format_exc()
        }
        return jsonify(error_details), 500

@app.route('/predictusg', methods=['POST'])
@require_api_key
def predictusg():

    # Oczekujemy danych wejściowych jako JSON z kluczem "image_base64"
    print('predictusg - enter')

    #print('request files: ', request.files.keys())
    #print('request data: ', request.get_data())

    #if 'file' not in request.files:
        #return jsonify({"error": "Brak pliku w żądaniu. Upewnij się, że wysyłasz plik z kluczem 'file'."}), 400

    try:

        #file = request.files['file']
        #image_b64 = request.get_data(as_text=True)
        #image_bytes = base64.b64decode(image_b64)
        image_bytes = request.get_data()
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        if MODEL_USG_PATH == 'breast_usg_model.keras':
            image = image.resize((150, 150))
        else:
            image = image.resize((200, 200))

        img_array = img_to_array(image)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Predykcja
        preds = modelUsg.predict(img_array)
        print('predictions', preds)
        predicted_index = np.argmax(preds, axis=1)[0]
        predicted_class = class_names[predicted_index]
        confidence = float(np.max(preds))

        return jsonify({
            'predicted_class': predicted_class,
            'confidence': confidence
        })

    except Exception as e:
        error_details = {
            "error": "Internal Server Error",
            "message": str(e),
            "trace": traceback.format_exc()
        }
        return jsonify(error_details), 500
@app.route('/models', methods=['GET'])
@require_api_key
def get_models():
    return jsonify({'files': list_models()})

if __name__ == '__main__':
    #port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=5000, debug=True)
