__author__ = 'wwang'

import mongoengine as mongo

class TwitterAccount(mongo.EmbeddedDocument):

    user_oauth_token = mongo.StringField(required = True)
    user_oauth_token_secret = mongo.StringField(required = True)

    def init(oauth_token, oauth_token_secret):
        user_oauth_token = oauth_token
        user_oauth_token_secret = oauth_token_secret

    def update(**kwargs):
        user_oauth_token = kwargs.get('user_oauth_token', '')
        user_oauth_token_secret = kwargs.get('user_oauth_token_secret', '')