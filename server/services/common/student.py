__author__ = 'wwang'

import mongoengine as mongo
from ..util.security import md5_hash

class Student(mongo.Document):

    meta = {
        'db_alias': 'user-db',
        'collection': 'students'
    }

    # The student's uwaterloo email
    email = mongo.StringField(required = True)

    # The student's password
    password_hash = mongo.StringField(required = True)

    # The year this student is in.
    current_year = mongo.StringField(required = True)

    # The current course plan.
    current_plan = mongo.ListField(required = True)

    # The current major.
    current_major = mongo.StringField(required = True)

    # The courses this student took before.
    # course - mark - year took - want to retake
    courses_taken = mongo.ListField(required = True)

    # The courses this student is interested in.
    interested_courses = mongo.ListField(required = True)

    def init(self, email, password):
        self.email = email
        self.password_hash = md5_hash(password)

        current_year = '1A'
        current_plan = []
        current_major = ''
        courses_taken = []
        interested_courses = []