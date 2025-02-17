from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import base64
from io import BytesIO
from PIL import Image
#import Image
import traceback
app = Flask(__name__)

# Ładowanie modelu (plik .h5 lub .keras)
model = tf.keras.models.load_model("pneumonia_classification_model.keras")


@app.route('/predict', methods=['POST'])
def predict():
    # Oczekujemy danych wejściowych jako JSON z kluczem "image_base64"
    print('predict - enter')

    print('request files: ', request.files.keys())
    print('request data: ', request.get_data())

    #if 'file' not in request.files:
        #return jsonify({"error": "Brak pliku w żądaniu. Upewnij się, że wysyłasz plik z kluczem 'file'."}), 400

    #file = request.files['file']
    #image_b64 = request.get_data(as_text=True)
    #image_bytes = base64.b64decode(image_b64)
    image_bytes = request.get_data()
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    image = image.resize((150, 150))
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predykcja
    prediction = model.predict(img_array)[0][0]
    label = "Pneumonia" if prediction > 0.5 else "Normal"
    print(jsonify({"prediction": float(prediction), "label": label}))
    return jsonify({"prediction": float(prediction), "label": label})
    '''
    except Exception as e:
        error_details = {
            "error": "Internal Server Error",
            "message": str(e),
            "trace": traceback.format_exc()
        }
        return jsonify(error_details), 500
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
