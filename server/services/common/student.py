__author__ = 'wwang'

import mongoengine as mongo
from twitter_account import TwitterAccount

class Student(mongo.Document):

    meta = {
        'db_alias': 'uw-tree',
        'collection': 'students'
    }

    # The twitter user id associated with this student account
    twitter_id = mongo.LongField(required = True)

    # The other twitter account infomation
    twitter_account = mongo.EmbeddedDocumentField(TwitterAccount, required = True)

    # Email
    email = mongo.StringField(required = True)

    # The year this student is in.
    current_year = mongo.StringField(required = True)

    # The current course plan.
    current_plan = mongo.ListField(required = True)

    # The current major.
    current_major = mongo.ListField(required = True)

    # The courses this student took before.
    # course - mark - year took - want to retake
    courses_taken = mongo.ListField(required = True)

    # The courses this student is interested in.
    interested_courses = mongo.ListField(required = True)

    def init(self, twitter_id, user_oauth_token, user_oauth_token_secret):
        self.twitter_id = twitter_id

        self.twitter_account = TwitterAccount()
        self.twitter_account.init(user_oauth_token, user_oauth_token_secret)

        self.current_year = '1A'
        self.current_plan = []
        self.current_major = []
        self.courses_taken = []
        self.interested_courses = []

    def update_twitter_info(self, **kwargs):
        self.twitter_account.update(**kwargs)

if __name__ == '__main__':
    student = Student()
    student.init('a', 'b', 'c')
    print student.twitter_account.user_oauth_token

