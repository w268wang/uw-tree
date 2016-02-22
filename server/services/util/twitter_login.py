__author__ = 'wwang'

from server import app
import oauth2 as oauth
import urllib2, urllib, urlparse
from ..database import mongo
from flask import make_response, redirect

app.config['TWITTER'] = {
    'CONSUMER_KEY': 'cml8hQQfMNswqnDd41KX8Z8PN',
    'CONSUMER_SECRET': '88W07O52ujOiGBjAOoLaF5bA9AdaUJWbZIPtXjd6lDf9TgmHmB',
    'ACCESS_TOKEN': '2772277171-bg3iBaMxhx42V6f6ZLVPKZAl3Hx7nGS8fww9S',
    'ACCESS_TOKEN_SECRET': '2tjnwKRjm0BaJDtgjM3Mz9UBUzmUFHK8fLOtkIWMVrUpk'
}

BASE_URL = 'http://127.0.0.1:5000'
tw_request_token_url = 'https://api.twitter.com/oauth/request_token'
tw_access_token_url = 'https://api.twitter.com/oauth/access_token'
oauth_info = {}

def twitter_oauth():
    app_callback_url = BASE_URL + "/twitter_callback"
    # app_callback_url = url_for("callback", _external = True)
    twitter_config = app.config['TWITTER']

    consumer = oauth.Consumer(twitter_config['CONSUMER_KEY'], twitter_config['CONSUMER_SECRET'])
    client = oauth.Client(consumer)
    resp, content = client.request(tw_request_token_url, "POST",
        body=urllib.urlencode({"oauth_callback": app_callback_url}))

    request_token = dict(urlparse.parse_qsl(content))
    oauth_token = request_token['oauth_token']
    oauth_token_secret = request_token['oauth_token_secret']
    return oauth_token, oauth_token_secret

def twitter_callback_handle(oauth_token, oauth_verifier, oauth_denied):
    app_callback_url = BASE_URL
    twitter_config = app.config['TWITTER']

    if oauth_denied:
        del oauth_info[oauth_token]
        res = make_response(redirect(app_callback_url))
        res.set_cookie("status", "1")
        return res

    oauth_token_secret = oauth_info[oauth_token]

    consumer = oauth.Consumer(twitter_config['CONSUMER_KEY'], twitter_config['CONSUMER_SECRET'])
    token = oauth.Token(oauth_token, oauth_token_secret)
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(tw_access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    user_id = access_token['user_id']
    user_oauth_token = access_token['oauth_token']
    user_oauth_token_secret = access_token['oauth_token_secret']

    user_exists = mongo.check_student_existence(user_id, "twitter")

    if not user_exists:
        mongo.add_student(user_id, user_oauth_token, user_oauth_token_secret)
    else:
        mongo.update_student_twitter_info(user_id, user_oauth_token, user_oauth_token_secret)

    del oauth_info[oauth_token]
    res = make_response(redirect(app_callback_url))
    res.set_cookie("id", user_id)
    res.set_cookie("token", user_oauth_token)
    res.set_cookie("secret", user_oauth_token_secret)
    res.set_cookie("status", "0")
    return res

if __name__ == '__main__':
    # print get_course_by_subject_and_catalog("CS", "246")
    print twitter_oauth()