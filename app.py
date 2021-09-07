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
model_base_url = 'http://3.38.9.213:5000'
main_base_url = 'http://3.34.215.157:3000'

@app.route('/', methods=["GET"])
def hello():
    return 'Hello, world'

@app.route("/")
def onego_hello():
    return "Welcome to ONEGO!"

@app.route("/file_download", methods=['POST','GET'])
def file_download():
    pred_list = ["원","고","지", " ", "인", "식", "이", " ", "돼", "어", "잇", "는", "파", "일", "입", "니", "다", "."]
    uid = request.args["uid"]
    file_path = './input/manuscript_input/{}.png'.format(uid)
    try:
        s3.download_file(AWS_S3_BUCKET_NAME,"{}/Pororo.png".format(uid),file_path)
        print("complete download .png from s3!")
        # pred_list = demo() --detect함수 실행하는 부분

        os.makedirs('./tmp', exist_ok=True)
        f = open('./tmp/{}.txt'.format(uid),'w',encoding='UTF-8')
        pred_str = ''.join(pred_list)
        f.write(pred_str)
        f.close()
        print('Complete create file')
        try:
            txt_path = './tmp/{}.txt'.format(uid)
            s3.upload_file(txt_path, AWS_S3_BUCKET_NAME, '{}/before_onego.txt'.format(uid))
            return("complete upload .txt to s3")
        except Exception as e:
            print(e)
            return "false upload .txt to s3"
    except Exception as e:
        print(e)
        return "flase download .png from s3..."


if __name__ == 'main':
    app.run(host="localhost",port=5000, debug=True)
