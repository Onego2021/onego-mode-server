# -- coding: utf-8 --

from flask import Flask, request, jsonify, url_for
import json, boto3, os
from werkzeug.utils import redirect, secure_filename
from aws_config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
s3 = boto3.client('s3',
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
)

@app.route('/', methods=["GET"])
def hello():
    return 'Hello, world'

@app.route("/")
def onego_hello():
    return "Welcome to ONEGO!"

@app.route("/onego_recognize", methods=['POST','GET'])
def onego_recognize():
    file = ""
    filename = ""
    path = "input/manuscript_input" + filename
    uid = request.args["uid"]

    if request.method == 'POST':
        file = request.file['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(path))

    elif request.method == 'GET':
        pred_list = ["원","고","지", " ", "인", "식", "이", " ", "돼", "어", "잇", "는", "파", "일", "입", "니", "다", "."]
        pred_str = ''.join(pred_list)
        os.makedirs('./tmp', exist_ok=True)
        f = open('./tmp/{}.txt'.format(uid),'w',encoding='UTF-8')
        print('Complete create file')
        f.write(pred_str)
        f.close()
        try:
            txt_path = './tmp/{}.txt'.format(uid)
            s3.upload_file(txt_path, AWS_S3_BUCKET_NAME, '{}/after_onego.txt'.format(uid))
            print("complete upload .txt to s3")
        except Exception as e:
            print(e)
            return "False..."
    
# @app.route("/test", methods=["GET"])
# def testPostAPI():
#     temp = request.args["uid"]
#     data = "test data"
#     return jsonify({
#         'result': data,
#         'uid' : temp,
#     })

@app.route("/file_download", methods = ["GET"])
def file_download():
    uid = request.args["uid"]
    file_path = './input/manuscript_input/{}.png'.format(uid)
    print(uid)
    try:
        s3.download_file(AWS_S3_BUCKET_NAME,"{}/Pororo.png".format(uid),file_path)
        print("complete download .png from s3!")
        return redirect(url_for('onego_recognize',uid = uid))
    except Exception as e:
        print(e)
        return "flase..."

if __name__ == 'main':
    app.run(host="localhost",port=5000, debug=True)
