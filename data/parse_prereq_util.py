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
REPLACEMENT_INIT_NUM = 100

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
    one_of_slash_sub_comma_category = 3
    slash_course = 4
    or_course = 5

SLASH_CATEGORY = r'([0-9]{3}[A-Z]?/)+[0-9]{3}[A-Z]?'
SLASH_SUB_COMMA_CATEGORY = r'(([A-Z]{2,6}/)+)?[A-Z]{2,6} ([0-9]{3}[A-Z]?, )+[0-9]{3}[A-Z]?'
SLASH_COURSE = r'([A-Z]{2,6} [0-9]{3}[A-Z]?/)+[A-Z]{2,6} [0-9]{3}[A-Z]?'
OR_COURSE = r'([A-Z]{2,6} [0-9]{3}[A-Z]? (OR|or) )+[A-Z]{2,6} [0-9]{3}[A-Z]?'
COURSE_PATTERN = r'[A-Z]{2,6} [0-9]{3}[A-Z]?'
CATEGORY_PATTERN = r'[0-9]{3}[A-Z]?'
SUBJECT_PATTERN = r'[A-Z]{2,6}'

def parse_course(course_string):

    course_string = re.sub(r'[0-9]{4}', '', course_string)
    print course_string

    result_course_list = []

    replace_array = [] # index = course category - replace_num
    course_string = _course_replacer(course_string, replace_array)

    print course_string
    # Grab all the courses left.
    while re.search(COURSE_PATTERN, course_string):
        valid_course_string = re.search(COURSE_PATTERN, course_string).group(0)
        course_string = course_string.replace(valid_course_string, ' ', 1)

        if re.search(r'[0-9]{3}Z', valid_course_string):

            parsed_subject_name = re.search(SUBJECT_PATTERN, valid_course_string).group(0)
            parsed_category = re.search(CATEGORY_PATTERN, valid_course_string).group(0)
            course_parse_result = _course_dereplacer(parsed_subject_name, parsed_category, replace_array)
            if isinstance(course_parse_result, basestring):
                result_course_list.append(course_parse_result)
            else:
                course_slash_splitted_string = ''
                for category_string in course_parse_result:
                    course_slash_splitted_string += '|' + parsed_subject_name + ' ' + category_string

                result_course_list.append(course_slash_splitted_string)

        else:
            parsed_subject_name = re.search(r'[A-Z]{2,6}', valid_course_string).group(0)
            parsed_category = re.search(r'[0-9]{3}[A-Y]?', valid_course_string).group(0)
            result_course_list.append(parsed_subject_name + ' ' + parsed_category)


    return result_course_list

def _course_replacer(course_string, replace_array):

    replace_num = REPLACEMENT_INIT_NUM

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
        replace_type = ReplaceType.slash_sub_comma_category

        course_part = re.search(SLASH_SUB_COMMA_CATEGORY, course_string).group(0)
        if re.search('(O|o)ne of ' + course_part, course_string):
            replace_type = ReplaceType.one_of_slash_sub_comma_category
            if re.search('one of ' + course_part, course_string):
                course_part = 'one of ' + course_part
            else:
                course_part = 'One of ' + course_part

        replace_course_string = 'REP ' + str(replace_num) + REPLACEMENT_CHAR

        course_string = course_string.replace(course_part, replace_course_string, 1)
        replace_array.append((replace_course_string, course_part, replace_type))
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

    return course_string

# replace_array: Constant parameter
def _course_dereplacer(subject_name, parsed_category, replace_array):

    def _unwire_slash_category(replaced_string):
        searched_category_list = []

        while re.search(CATEGORY_PATTERN, replaced_string):
            searched_category_string = re.search(CATEGORY_PATTERN, replaced_string).group(0)
            replaced_string = replaced_string.replace(searched_category_string, ' ', 1)
            searched_category_list.append(searched_category_string)
        return searched_category_list

    print 'get ' + subject_name + ' with ' + parsed_category
    replaced_course_tuple = replace_array[int(parsed_category[:-1]) - REPLACEMENT_INIT_NUM]
    replace_course_string = replaced_course_tuple[1]
    replace_type = replaced_course_tuple[2]
    if replace_type == ReplaceType.or_course or \
        replace_type == ReplaceType.slash_course:

        result_string = ''
        searched_course_list = []

        while re.search(COURSE_PATTERN, replace_course_string):
            searched_course_string = re.search(COURSE_PATTERN, replace_course_string).group(0)
            replace_course_string = replace_course_string.replace(searched_course_string, ' ', 1)
            searched_course_list.append(searched_course_string)

        for searched_course in searched_course_list:
            replaced_category_string = re.search(CATEGORY_PATTERN, searched_course).group(0)
            if searched_course[-1:] == REPLACEMENT_CHAR:
                dereplace_result = _course_dereplacer(subject_name, replaced_category_string, replace_array)
                if isinstance(dereplace_result, basestring):
                    result_string += '|' + dereplace_result
                else:
                    subject_string = re.search(SUBJECT_PATTERN, searched_course).group(0)
                    for category_string in dereplace_result:
                        result_string += '|' + subject_string + ' ' + category_string
            else:
                result_string += '|' + searched_course
        return result_string

    elif replace_type == ReplaceType.slash_sub_comma_category or \
        replace_type == ReplaceType.one_of_slash_sub_comma_category:

        result_string = ''
        searched_category_list = []

        subject_string = re.search(SUBJECT_PATTERN, replace_course_string).group(0)
        while re.search(CATEGORY_PATTERN, replace_course_string):
            searched_category_string = re.search(CATEGORY_PATTERN, replace_course_string).group(0)
            replace_course_string = replace_course_string.replace(searched_category_string, ' ', 1)
            if searched_category_string[-1:] == REPLACEMENT_CHAR:
                replaced_category_tuple = replace_array[int(searched_category_string[:-1]) - REPLACEMENT_INIT_NUM]
                replace_category_string = replaced_category_tuple[1]
                searched_category_list.extend(_unwire_slash_category(replace_category_string))
            else:
                searched_category_list.append(searched_category_string)

        for category_string in searched_category_list:
            result_string += '|' + subject_string + ' ' + category_string

        if replace_type == ReplaceType.one_of_slash_sub_comma_category:
            result_string = str(len(searched_category_list)) + result_string

        return result_string

    elif replace_type == ReplaceType.slash_category:

        return _unwire_slash_category(replace_course_string)
    else:

        raise BaseException(202)


if __name__ == '__main__':
    # print parse_course('One of ECE 316, 318, Level at least 4A Computer Engineering or Electrical Engineering')
    print parse_course('AAA 100, 200R, 300 or BBB 100/CCC 200, AMATH 242/341/CM 271/CS 371, DDD 111/222, EEE 111/222, RRR 100S')
    # print re.search(CATEGORY_PATTERN, 'REP 103Z').group(0)
