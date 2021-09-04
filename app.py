# -- coding: utf-8 --

from flask import Flask, request, jsonify
import os
import json

from werkzeug.utils import secure_filename
# from util.manuscript_recognizer import start_recognize
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def onego_hello():
    return "Welcome to ONEGO!"

@app.route("/onego_recognize", methods=['POST','GET'])
def onego_recognize():
    file = ""
    filename = ""
    path = "input/manuscript_input" + filename

    if request.method == 'POST':
        file = request.file['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(path))
    elif request.method == 'GET':
        pred_list = ["원","고","지", " ", "인", "식", "이", " ", "돼", "어", "잇", "는", "파", "일", "입", "니", "다", "."]
        # pred_list = start_recognize(path)
        return jsonify({"predList":pred_list})
    
@app.route("/test", methods=["GET"])
def testPostAPI():
    temp = request.args["uid"]
    data = "test data"
    return jsonify({
        'result': data,
        'uid' : temp,
    })

if __name__ == 'main':
    app.run(host="localhost",port=5000, debug=True)
