__author__ = 'wwang'

from server import app
from flask import Response, request
from services.database import mongo
from services.util.twitter_login import twitter_oauth, twitter_callback_handle
import json

@app.route('/')
def index():
    return 'Hello World!'


def build_response(json_obj, code = 200):
    return Response(response = json_obj, status = code,
                    mimetype="application/json")

def build_empty_response(code = 200):
    return Response(status = code)

@app.route('/get/course/<subject>/<catalog>', methods=['GET'])
def get_course(subject, catalog):
    result = mongo.get_course_by_subject_and_catalog(subject, catalog)
    return build_response(result)

@app.route('/add/student/<twitter_id>', methods=['GET'])
def add_student(twitter_id):
    mongo.add_student(twitter_id)
    return build_empty_response()

@app.route('/update/student/', methods=['POST'])
def update_student():
    name = request.form['name']
    email = request.form['email']

# redirect to https://twitter.com/oauth/authorize?oauth_token=
@app.route("/twitterreqoauth", methods=['GET'])
def get_twitter_req_oauth():
    oauth_token = twitter_oauth()
    return json.dumps({"token": oauth_token})

@app.route("/twitter_callback", methods=['GET'])
def get_twitter_credentials():
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    oauth_denied = request.args.get('denied')
    return twitter_callback_handle(oauth_token, oauth_verifier, oauth_denied)