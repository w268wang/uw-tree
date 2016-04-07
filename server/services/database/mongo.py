__author__ = 'wwang'

from mongoengine import connect
from mongoengine import *
from server.services.common.student import Student
from server.services.common.course import Course
from server.services.common.twitter_account import TwitterAccount
from bson import json_util

connection = connect(db = 'uw-tree', alias = 'uw-tree')

class Page(Document):
    meta = {
        'db_alias': 'uw-tree',
        'collection': 'test'
    }
    title = StringField(required = False)

def insert_list(course_object_list, class_type):
    print course_object_list[0]['evaluated_prereq']
    class_type.objects.insert(course_object_list)

def get_course_by_subject_and_catalog(subject, catalog):
    result = Course.objects.get(name = subject + ' ' + catalog)
    return result.to_json()

def get_course_by_name(name):
    result = Course.objects.get(name = name)
    return result.to_json()

def update_course_by_field(match_query, update_content):
    result = Course.objects.modify(query = match_query, update = update_content)
    return result.to_json()

def check_student_existence(twitter_id_input):
    try:
        student = Student.objects.get(twitter_id = twitter_id_input)
    except Student.DoesNotExist:
        return False
    return student != None

def add_student(twitter_id, user_oauth_token, user_oauth_token_secret):
    student = Student()
    student.init(twitter_id, user_oauth_token, user_oauth_token_secret)
    Student.objects.insert(student)

def update_student_twitter_info(twitter_id, user_oauth_token = '', user_oauth_token_secret = ''):
    if len(user_oauth_token):
        Student.objects(twitter_id = twitter_id)\
            .update_one(set__twitter_account__user_oauth_token = user_oauth_token)

    if len(user_oauth_token_secret):
        Student.objects(twitter_id = twitter_id)\
            .update_one(set__twitter_account__user_oauth_token_secret = user_oauth_token_secret)

def update_student_info(twitter_id, **modify):
    Student.objects(twitter_id = twitter_id).update_one(**modify)


if __name__ == '__main__':
    # print get_course_by_subject_and_catalog("CS", "246")
    # print update_course_by_field({'name': 'CS 246'}, {'teapot_prereq': {'a': 1}})
    # update_student_twitter_info('2772277171', 'a2', 'b3')
    #update_student_info(twitter_id='2772277171', current_year = 'a2', courses_taken = ['b3', 'c'])
    update_student_info(twitter_id='2772277171', current_year = '3A', courses_taken = ['b3', 'c'],
                        interested_courses = ['CS 452', 'CS 488s'])

