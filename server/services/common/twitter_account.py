__author__ = 'wwang'

import mongoengine as mongo

class TwitterAccount(mongo.EmbeddedDocument):

    user_oauth_token = mongo.StringField(required = True)
    user_oauth_token_secret = mongo.StringField(required = True)

    def init(self, oauth_token, oauth_token_secret):
        self.user_oauth_token = oauth_token
        self.user_oauth_token_secret = oauth_token_secret

    def update(self, **kwargs):
        self.user_oauth_token = kwargs.get('user_oauth_token',
                                           self.user_oauth_token)
        self.user_oauth_token_secret = kwargs.get('user_oauth_token_secret',
                                                  self.user_oauth_token_secret)