from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
from flask_cors import CORS
import base64

app = Flask(__name__)

CORS(app)

model = load_model('model.h5')

def process_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB') 
    image = image.resize((224, 224)) 
    image = np.array(image) / 255.0 
    image = np.expand_dims(image, axis=0) 
    return image

@app.route('/predict', methods=['POST'])
def predict():
    print("called")
    data = request.get_json()

    if 'image' not in data:
        return jsonify({'error': 'No image'})

    image = data['image']
    try:
        image = io.BytesIO(base64.b64decode(image))
        image = process_image(image.read())
        
        predictions = model.predict(image)
        predictedClass = (predictions > 0.5).astype(int)[0][0]
        
        classNames = {0: 'NORMAL', 1: 'PNEUMONIA'}
        result = classNames[predictedClass]
        print("Result ", result)
        return jsonify({'prediction': result})
    except Exception as e:
        print(e)
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)
