from flask import Flask, request, jsonify
import json, boto3, os
from aws_config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME
# from aws_connect import s3_connection, s3_get_object
app = Flask(__name__)
s3 = boto3.client('s3',
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
)

@app.route('/', methods=["GET"])
def hello():
    return 'Hello, world'

@app.route("/onego_detect", methods=["POST"])
def onego_detect():
    image = "onego_detect"
    return image

@app.route("/onego_recognize", methods=["GET"])
def onego_recognize():
    image = "onego_recognize"
    return image

@app.route("/test", methods=["GET"])
def testPostAPI():
    temp = request.args["uid"]
    data = {'txt' : "test data", 'uid' : temp}
    return jsonify(data)

@app.route("/file_download", methods = ["GET"])
def file_download():
    uid = request.args["uid"]
    file_path = './input/manuscript_input/{}.png'.format(uid)
    print(uid)
    try:
        s3.download_file(AWS_S3_BUCKET_NAME,"{}/Pororo.png".format(uid),file_path)
        return "complete download"
    except Exception as e:
        print(e)
        return "flase..."

if __name__ == 'main':
    app.run(host="localhost",port=5000, debug=True)
