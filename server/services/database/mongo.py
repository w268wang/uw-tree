__author__ = 'wwang'

from mongoengine import connect
from mongoengine import *
from server.services.common.student import Student
from server.services.common.course import Course
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

def update_course_by_field(match_query, update_content):
    result = Course.objects.modify(query = match_query, update = update_content)
    return result.to_json()

def add_student(twitter_id):
    student = Student(twitter_id)
    Student.objects.insert(student)


if __name__ == '__main__':
    # print get_course_by_subject_and_catalog("CS", "246")
    print update_course_by_field({'name': 'CS 246'}, {'teapot_prereq': {'a': 1}})

