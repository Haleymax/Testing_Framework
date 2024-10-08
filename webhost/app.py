from flask import Flask, request, jsonify

from webhost.api.app import hello_world

app = Flask(__name__)


app.run("127.0.0.1", 8080, debug=True)