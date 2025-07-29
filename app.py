import os
import numpy as np
from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from PIL import Image
from arabic_mapping import get_arabic_letter

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = load_model("model.h5")

def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')
    img = img.resize((32, 32))
    img = np.array(img)
    img = np.rot90(img, k=3)  
    img = np.fliplr(img)
    img = img.reshape(1, 32, 32, 1)
    img = img.astype('float32') / 255.0
    return img

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        file = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        image = preprocess_image(filepath)
        pred = model.predict(image)
        class_index = np.argmax(pred)
        prediction = get_arabic_letter(class_index + 1)  

        return render_template('index.html', prediction=prediction, image=file.filename)
    
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
