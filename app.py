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
    print('request: ', request.get_data())
    #data = request.get_json(force=True)
    #image_b64 = data.get("image_base64")
    image_b64 = request.get_data(as_text=True)


    print(image_b64)
    if not image_b64:
        return jsonify({"error": "Brak 'image_base64' w danych wejściowych"}), 400

    #try:
    # Dekodowanie base64 do obrazu
    image_bytes = base64.b64decode(image_b64)
    print("Rozmiar danych obrazu (w bajtach):", len(image_bytes))
    # Próba otwarcia obrazu
    image_stream = BytesIO(image_bytes)
    image = Image.open(image_stream)

    # Weryfikacja obrazu – sprawdzenie integralności
    image.verify()  # Uwaga: po wywołaniu verify() obraz nie może być już dalej użyty
    # Przywrócenie strumienia do początku
    image_stream.seek(0)
    image = Image.open(image_stream).convert("RGB")

    image = image.resize((150, 150))
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predykcja
    prediction = model.predict(img_array)[0][0]
    label = "Pneumonia" if prediction > 0.5 else "Normal"
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
    app.run(debug=True)
