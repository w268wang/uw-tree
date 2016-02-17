__author__ = 'wwang'

from uwaterlooapi import UWaterlooAPI
import re
import os
import json

uw = UWaterlooAPI(api_key="7d435b989e48df6956b88dd5248b13dc")
VALID_DEP = ['AHS', 'ART', 'ENG', 'ENV', 'MAT', 'SCI', 'REN', 'VPA', 'WLU']
CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/'

SUBJECT_LIST_FILE = 'subject_list.txt'
COURSE_CAT_FILE = 'courses.txt'
COURSE_DETAIL_FILE = 'courses_detailed_data.txt'
PREREQ_LIST_FILE = 'courses_prereq.txt'

# TODO actually use open api
def update_courses_file():
    '''
    Output: Output will get written into a file for future use
            each line represents courses for a subject, items are splitted by '|'
            the first item is the subject name and the others are course categories
    Example: APPLS|205R|301|304R|306R
    '''

    # Get subject code from uwaterloo api endpoint (/codes/subjects.json).
    #raw_subject_list = uw.subject_codes()

    # Filter out all the subjects with valid department category.
    #valid_raw_subject_list = filter(lambda item: item['group'] in VALID_DEP, raw_subject_list)

    # Retrieve the subject field out of the data
    #subject_list = map(lambda item: item['subject'], valid_raw_subject_list)

    with open(CURRENT_FOLDER + SUBJECT_LIST_FILE, 'r') as subject_list_file:
        subject_list = subject_list_file.read().splitlines()

    # Output file for course list
    courses_output_file = open(CURRENT_FOLDER + COURSE_CAT_FILE, 'w')
    ctr = 0
    for subject in subject_list:
        courses_data = uw.courses(subject)
        is_undergrduate_subject = True

        if len(courses_data) > 0:
            first_digit = int(courses_data[0]['catalog_number'][0:1])
            category_len = len(courses_data[0]['catalog_number'])
            is_undergrduate_subject = not (first_digit > 5 and category_len > 2)

        if len(courses_data) > 0 and is_undergrduate_subject:
            ctr += 1

            courses_output_file.write(subject)
            for course_info in courses_data:
                courses_output_file.write('|' + str(course_info['catalog_number']))
            courses_output_file.write('\n')

    print "Get courses for " + str(len(subject_list)) + " subjects."


def get_course_detail():
    '''
    Repeatedly call the courses API for details of every single course

    Output: output gets written into an specified output file as dumped dictionary object
            one can easily load using the following code:
    with open(CURRENT_FOLDER + COURSE_DETAIL_FILE, 'r') as courses_input_file:
        course_detail_data = eval(courses_input_file.read())
    '''
    ctr = 0
    course_dic = {}

    with open(CURRENT_FOLDER + COURSE_CAT_FILE, 'r') as courses_input_file:
        file_content = courses_input_file.read().splitlines()
        for line in file_content:
            line_arr = line.split('|')
            subject_name = line_arr[0]
            course_category_list = line_arr[1:]

            detail = []
            for course_category in course_category_list:
                detail.append(uw.course(subject_name, course_category))
                ctr += 1
                print ctr

            course_dic[subject_name] = detail

        courses_detailed_data = open(CURRENT_FOLDER + COURSE_DETAIL_FILE, 'w')
        courses_detailed_data.write(str(course_dic))

    print "Get info for " + str(ctr) + " courses."


def translate_prerequisits():

    prerequisit_description_list = []
    with open(CURRENT_FOLDER + COURSE_DETAIL_FILE, 'r') as courses_input_file:
        course_detail_data = eval(courses_input_file.read())
        for subject_name in course_detail_data.keys():
            load_error_count = 0
            for course_item in course_detail_data[subject_name]:
                try:
                    if course_item['prerequisites']:
                        prerequisit_description_list.append(course_item['prerequisites'])
                except:
                    load_error_count += 1
                    continue
            if load_error_count:
                print 'Failed to load ' + str(load_error_count) + ' course(s) for ' + subject_name

    #with open(CURRENT_FOLDER + PREREQ_LIST_FILE, 'w') as prereq_output_file:
    for prereq in prerequisit_description_list:
        #prereq_output_file.write(prereq + '\n')
        parse_prereq(prereq)

    print len(global_section_ctr)
    print len(school_year_ctr)


if __name__ == '__main__':
    # update_courses_file()
    # get_course_detail()
    translate_prerequisits()
