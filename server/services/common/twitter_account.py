__author__ = 'wwang'

import mongoengine as mongo

class TwitterAccount(mongo.EmbeddedDocument):

    # Placeholder
    twitter_id = mongo.LongField(required = True)