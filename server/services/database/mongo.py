__author__ = 'wwang'

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from mongoengine import connect
from mongoengine import *
from server.services.common.student import Student
from server.services.common.course import Course

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

def get_course_by_name():
    print Course.objects.get(name = "CS 246")

if __name__ == '__main__':
    get_course_by_name()

