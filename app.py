# -- coding: utf-8 --

from flask import Flask, request, jsonify, url_for
import json, boto3, os
from werkzeug.utils import redirect, secure_filename
from aws_config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME
from util.manuscript_recognizer import start_recognize

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
    img_path = "/home/ubuntu/onego-model-server/input/manuscript_input/onego2.png"
    start_recognize(img_path)
    return "Wellcome onego-model-server!!"

@app.route("/")
def onego_hello():
    return "Welcome to ONEGO!"

@app.route("/file_download", methods=['POST','GET'])
def file_download():
    uid = request.args["uid"]
    file_path = '/home/ubuntu/onego-model-server/input/manuscript_input/{}.png'.format(uid)
    try:
        s3.download_file(AWS_S3_BUCKET_NAME,"{}/Pororo.png".format(uid),file_path)
        print("complete download .png from s3!")
        pred_list = start_recognize('/home/ubuntu/onego-model-server/input/manuscript_input/{}.png'.format(uid))

        os.makedirs('./tmp', exist_ok=True)
        f = open('./tmp/{}.txt'.format(uid),'w',encoding='UTF-8')
        f.write(pred_list)
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
        return "false download .png from s3..."


if __name__ == 'main':
    app.run(host="0.0.0.0",port=5000, debug=True)
