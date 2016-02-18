__author__ = 'wwang'

from server import app
import json

@app.route('/')
def index():
    return 'Hello World!'


@app.route('/get/course')
def get_course():
    return json.dumps({})