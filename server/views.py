__author__ = 'wwang'

from server import app
from flask import Response, request
import flask
from services.database import mongo
import json

@app.route('/')
def index():
    return 'Hello World!'


def build_response(json_obj, code = 200):
    return Response(response = json_obj, status = code,
                    mimetype="application/json")

@app.route('/get/course/<subject>/<catalog>', methods=['GET'])
def get_course(subject, catalog):
    result = mongo.get_course_by_subject_and_catalog(subject, catalog)
    return build_response(result)