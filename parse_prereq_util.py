__author__ = 'wwang'

import re
import os
from enum import Enum

#############################################################
# IMPORTANT ASSUMPTION: course category never ends with 'Z' #
#############################################################

VALID_DEP = ['AHS', 'ART', 'ENG', 'ENV', 'MAT', 'SCI', 'REN', 'VPA', 'WLU']
CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/'
REPLACEMENT_CHAR = 'Z'

SUBJECT_LIST_FILE = 'subject_list.txt'
COURSE_CAT_FILE = 'courses.txt'
COURSE_DETAIL_FILE = 'courses_detailed_data.txt'
PREREQ_LIST_FILE = 'courses_prereq.txt'

global_section_ctr = []
school_year_ctr = []


course_dic = {}
with open(CURRENT_FOLDER + COURSE_CAT_FILE, 'r') as courses_input_file:
    file_content = courses_input_file.read().splitlines()
    for line in file_content:
        line_arr = line.split('|')
        subject_name = line_arr[0]
        course_category_list = line_arr[1:]
        course_dic[subject_name] = course_category_list

def parse_prereq(prereq_string):
    '''

    :param prereq_string:
    :return: None when it is unparsable and need human tagging
             Dictionary:
                course_pre:
                major_pre
    '''
    if '; or' in prereq_string:
        return None

    if re.search(r'\([^\)]*;.*\)', prereq_string): # eng special (;) semi-colon inside brackets
        #TODO
        return None
    prereq_dic = {}
    prereq_array = prereq_string.split(';')
    for prereq_element in prereq_array:
        global_section_ctr.append("")

        if re.search(r'( |^|\()[1-4][aAbB]', prereq_element): # contains school year info
            if re.search(r'((\(.+\)) or)+ \(.+\)', prereq_element): # () or... ()
                pass
            elif re.search(r'\([^)]*and.*\)', prereq_element): # (and)
                pass
            elif re.search(r'\(\(', prereq_element): # (()and())
                pass
            elif re.search(r'[0-9]{3}', prereq_element):
                and_split = prereq_element.split('and')
                for and_split_element in and_split:
                    for or_split_element in and_split_element.split('or'):
                        if re.search(r'( |^|\()[1-4][aAbB]', prereq_element) \
                                and re.search(r'[0-9]{3}', prereq_element):
                            return None
                        elif re.search(r'( |^|\()[1-4][aAbB]', prereq_element):
                            print prereq_element
                        elif re.search(r'[0-9]{3}', prereq_element):
                            pass
                print prereq_element
                school_year_ctr.append("")

class ReplaceType(Enum):
    slash_category = 1
    slash_sub_comma_category = 2
    slash_course = 3
    or_course = 4

SLASH_CATEGORY = r'([0-9]{3}[A-Z]?/)+[0-9]{3}[A-Z]?'
SLASH_SUB_COMMA_CATEGORY = r'(([A-Z]{2,6}/)+)?[A-Z]{2,6} ([0-9]{3}[A-Z]?, )+[0-9]{3}[A-Z]?'
SLASH_COURSE = r'([A-Z]{2,6} [0-9]{3}[A-Z]?/)+[A-Z]{2,6} [0-9]{3}[A-Z]?'
OR_COURSE = r'([A-Z]{2,6} [0-9]{3}[A-Z]? (OR|or) )+[A-Z]{2,6} [0-9]{3}[A-Z]?'
COURSE_PATTERN = r'[A-Z]{2,6} [0-9]{3}[A-Z]?'

def parse_course(course_string):

    course_string = re.sub(r'[0-9]{4}', '', course_string)
    print course_string

    replace_num = 100
    replace_array = [] # index = course category - replace_num
    result_course_list = []

    # Replace / divided category. e.g. 123/345A/275 to 100Z
    while re.search(SLASH_CATEGORY, course_string):
        replace_category_string = str(replace_num) + REPLACEMENT_CHAR
        category_part = re.search(SLASH_CATEGORY, course_string).group(0)
        course_string = course_string.replace(category_part, replace_category_string, 1)
        replace_array.append((replace_category_string, category_part, ReplaceType.slash_category))
        replace_num += 1

    print course_string
    # Replace / divided subject and , divided category. e.g. SOC/LS 280, 321 to REP 101Z
    while re.search(SLASH_SUB_COMMA_CATEGORY, course_string):
        replace_course_string = 'REP ' + str(replace_num) + REPLACEMENT_CHAR
        course_part = re.search(SLASH_SUB_COMMA_CATEGORY, course_string).group(0)
        course_string = course_string.replace(course_part, replace_course_string, 1)
        replace_array.append((replace_course_string, course_part, ReplaceType.slash_sub_comma_category))
        replace_num += 1

    print course_string
    # Replace / divided course. e.g. SOC 123/LS 280 to REP 101Z
    while re.search(SLASH_COURSE, course_string):
        replace_course_string = 'REP ' + str(replace_num) + REPLACEMENT_CHAR
        course_part = re.search(SLASH_COURSE, course_string).group(0)
        course_string = course_string.replace(course_part, replace_course_string, 1)
        replace_array.append((replace_course_string, course_part, ReplaceType.slash_course))
        replace_num += 1

    print course_string
    # Replace OR divided course. e.g. SOC 123 OR LS 280 to REP 101Z
    while re.search(OR_COURSE, course_string):
        replace_course_string = 'REP ' + str(replace_num) + REPLACEMENT_CHAR
        course_part = re.search(OR_COURSE, course_string).group(0)
        course_string = course_string.replace(course_part, replace_course_string, 1)
        replace_array.append((replace_course_string, course_part, ReplaceType.or_course))
        replace_num += 1

    print course_string
    # Grab all the courses left.
    while re.search(COURSE_PATTERN, course_string):
        valid_course_string = re.search(COURSE_PATTERN, course_string).group(0)
        course_string = course_string.replace(valid_course_string, ' ', 1)

        if re.search(r'[0-9]{3}Z', valid_course_string):
            result_course_string = ''
            parsed_subject_name = re.search(r'[A-Z]{2,6}', valid_course_string).group(0)
            parsed_category = re.search(r'[0-9]{3}Z?', valid_course_string).group(0)
            print 'get ' + parsed_subject_name + ' with ' + parsed_category
            replaced_course_tuple = replace_array[int(parsed_category[:-1]) - replace_num]
            
            print replace_array[int(parsed_category[:-1]) - replace_num]

        else:
            parsed_subject_name = re.search(r'[A-Z]{2,6}', valid_course_string).group(0)
            parsed_category = re.search(r'[0-9]{3}[A-Y]?', valid_course_string).group(0)
            print 'get ' + parsed_subject_name + ' with ' + parsed_category


    return result_course_list

if __name__ == '__main__':
    #print parse_course('One of ECE 316, 318, Level at least 4A Computer Engineering or Electrical Engineering')
    print parse_course('AAA 100, 200R, 300 or BBB 100/CCC 200, AMATH 242/341/CM 271/CS 371, DDD 111/222, EEE 111/222, RRR 100S')

