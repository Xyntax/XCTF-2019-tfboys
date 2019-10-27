# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import send_file
from flask import render_template
import os
import zipfile
import tensorflow as tf
from keras.preprocessing import sequence
import pickle

print(tf.__version__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

MODEL_DEFAULT = os.path.realpath('model/default')
MODEL_UPLOAD = os.path.realpath('model/upload')
TOKENIZER = os.path.realpath('build/tokenizer')
ZIP_TEMP = '/tmp/temp.zip'


class TF_MODEL:
    def __init__(self, path):
        self.load(path)
        self.tokenizer = pickle.load(open(TOKENIZER, 'rb'))
        self.TOKEN_LEN = 512
        self.THRESHOLD = 0.9

    def load(self, path):
        self.model_path = path
        self.session = tf.Session(graph=tf.Graph())
        meta_graph_def = tf.saved_model.loader.load(self.session, [tf.saved_model.SERVING], path)
        signature = meta_graph_def.signature_def
        x_tensor_name = signature['serving_default'].inputs['input'].name
        y_tensor_name = signature['serving_default'].outputs['output'].name
        self.x = self.session.graph.get_tensor_by_name(x_tensor_name)
        self.y = self.session.graph.get_tensor_by_name(y_tensor_name)

    def tokenize(self, content):
        X = self.tokenizer.texts_to_sequences(content)
        return sequence.pad_sequences(X, maxlen=self.TOKEN_LEN)

    def predict(self, content):
        X = self.tokenize([content])
        score = self.session.run(self.y, feed_dict={self.x: X})
        return True if score > self.THRESHOLD else False

    def get_model_path(self):
        return self.model_path


model = TF_MODEL(MODEL_DEFAULT)
print('loading model from ' + MODEL_DEFAULT + ' finished.')


@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    content = request.form.get('content')
    if request.method == 'POST' and content:  # disable captcha
        message = 'Malicious Content' if model.predict(content) else 'Legal Content'

    return render_template(
        'index.html',
        message=message,
        model_msg='loaded model: ' + model.get_model_path()
    )


@app.route('/model_upload', methods=['POST'])
def upload():
    file = request.files.get('files')
    if not file:
        return 'invalid zip file.'

    file.save(ZIP_TEMP)

    r = zipfile.is_zipfile(ZIP_TEMP)
    if not r:
        return 'invalid zip file.'

    fz = zipfile.ZipFile(ZIP_TEMP, 'r')
    extract_list = [
        'saved_model.pb',
        'variables/'
    ]

    namelist = fz.namelist()
    for each in namelist:
        if (each not in extract_list and not each.startswith('variables/')) or '../' in each:
            return 'Invalid tensorflow saved_model format, use "zip -r model.zip saved_model.pb variables/" to generate zip file then upload.'
    else:
        fz.extractall(MODEL_UPLOAD)
        try:
            model.load(MODEL_UPLOAD)
        except Exception as err:
            model.load(MODEL_DEFAULT)
            return "Fail to load model. tf.__version__: 1.14.0 <br> Exception: {0}".format(err)
        return 'Load new model success.'


@app.route('/model_download', methods=['GET'])
def download():
    name = 'model.zip'
    current_model_dir = model.get_model_path()
    zip_path = os.path.join(current_model_dir, name)
    if os.path.isfile(zip_path):
        os.remove(zip_path)
    zipcmd = 'cd {} && zip -r {} saved_model.pb variables/'.format(current_model_dir, name)
    os.system(zipcmd)
    return send_file(zip_path)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5679,
        debug=False
    )

