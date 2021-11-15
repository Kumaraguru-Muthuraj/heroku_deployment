from __future__ import division, print_function

# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# importing required modules
from zipfile import ZipFile
import joblib

app = Flask(__name__)

def unzipPklFile():
    # specifying the zip file name
    file_name = "userFinalRating.zip"

    # opening the zip file in READ mode
    with ZipFile(file_name, 'r') as zip:
        zip.extractall()

unzipPklFile()
ratingsMatrix = joblib.load('userFinalRating.pkl')
productClass = joblib.load('product_class.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if (request.method == 'POST'):
        formVals = [x for x in request.form.values()]
        usrName = formVals[0].lower()
        try:
            top20UserBased = ratingsMatrix.loc[usrName].sort_values(ascending=False)[0:20]
            for itmName in list(top20UserBased.index):
                top20UserBased[itmName] = productClass.loc[itmName][0]

            top5 = list(top20UserBased.sort_values(ascending=False)[:5].index)
            res = ""
            idx = 1
            for itm in top5:
                res += "({0}) {1}\n\n".format(idx, itm)
                idx += 1

            return render_template('index.html', items_list="Top 5 items recommended are {0}".format(res))
        except Exception:
            return render_template('index.html', items_list="User doesn't exist")
    else:
        return render_template('index.html')

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)
    app.debug=True
    app.run()
