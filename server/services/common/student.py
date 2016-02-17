__author__ = 'wwang'

import mongoengine as mongo

class Student(mongo.Document):

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