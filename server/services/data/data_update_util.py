__author__ = 'wwang'

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(__file__))

from server.services.database import mongo
from server.services.common.course import Course
import os

CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/'

COURSE_DETAIL_FILE = 'courses_detailed_data.txt'

def upload_courses():
    course_object_list = []
    with open(CURRENT_FOLDER + COURSE_DETAIL_FILE, 'r') as courses_input_file:
        course_detail_data = eval(courses_input_file.read())
        for subject_name in course_detail_data.keys():
            load_error_count = 0
            for course_item in course_detail_data[subject_name]:
                try:
                    course = Course()
                    course.setup(course_item)
                    course_object_list.append(course)
                except:
                    load_error_count += 1
                    continue

            if load_error_count:
                print 'Failed to load ' + str(load_error_count) + ' course(s) for ' + subject_name
    mongo.insert_list(course_object_list, Course)


if __name__ == '__main__':
    upload_courses()