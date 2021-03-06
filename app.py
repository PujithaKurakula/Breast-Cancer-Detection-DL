

import os
from tensorflow.keras.models import load_model
import numpy as np
from flask import Flask, request, send_from_directory,render_template,Response
from keras.preprocessing import image
from werkzeug.utils import secure_filename
app = Flask(__name__)
model_path="model/model.h5"
model=load_model(model_path,compile=False)
def model_predict(img_path, model):
    test_image=image.load_img(img_path,target_size=(50,50))
    test_image=image.img_to_array(test_image)
    test_image=np.expand_dims(test_image,axis=0)
    res=model.predict(test_image)[0][0]
    return res
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/help')
def form():
    return render_template('help.html')
@app.route('/predict', methods=["GET","POST"])
def predict():
    if request.method == 'POST':
        file = request.files['image_file']
        basepath=os.path.dirname(__file__)
        filename=secure_filename(file.filename)
        filepath=os.path.join(basepath,'uploads/',file.filename)
        file.save(filepath)
        livepreds = model_predict(filepath,model)
        if livepreds==1:
            return render_template('withoutcancer.html',filename=filename)
        else:
            return render_template('withcancer.html',filename=filename)
    return None

@app.route('/predict/<filename>')
def send_image(filename):
    return send_from_directory("uploads", filename)
if __name__ == '__main__':
          app.run()
          
        

