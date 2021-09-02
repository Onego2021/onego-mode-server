from flask import Flask, request, jsonify
import json
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def main():
    return 'Hello, world'

@app.route("/onego_recognize", methods=["GET"])
def onego_recognize():
    image = "onego_recognize"
    return image

if __name__ == 'main':
    app.run(host="localhost",port=8000, debug=True)