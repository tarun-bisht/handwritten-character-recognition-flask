from flask import Flask, url_for, render_template,request,jsonify
import json
import tensorflow as tf
import numpy as np
app = Flask(__name__)
global graph
path="models/conv_model.h5"
model=tf.keras.model.load_model(path)
graph=tf.get_default_graph()
def prediction(data):
	with graph.as_default():
		pred=model.predict(data)
		return pred
@app.route("/")
def index():
    title="Recognition"
    return render_template('pages/home.html',title=title)
@app.route("/about")
def about():
    title="About"
    return render_template('pages/about.html',title=title)
@app.route("/predict",methods=['POST'])
def predict():
    pixel=request.form.to_dict()
    data=json.loads(pixel.get("pixels"))
    variable=np.array(data).reshape(1,28,28,1)
	pred=prediction(variable)
	p=np.argmax(pred)
	resp={'prediction':int(p)}
	return jsonify(resp)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
