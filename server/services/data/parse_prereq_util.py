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

SLASH_CATEGORY = r'([0-9]{3}[A-Z]?/)+[0-9]{3}[A-Z]?' # 100R/234A
SLASH_SUB_COMMA_CATEGORY = r'(([A-Z]{2,6}/)+)?[A-Z]{2,6} ([0-9]{3}[A-Z]?, )+[0-9]{3}[A-Z]?' # AAA/BBB 123, 342
SLASH_COURSE = r'([A-Z]{2,6} [0-9]{3}[A-Z]?/)+[A-Z]{2,6} [0-9]{3}[A-Z]?' # XXX 100/XXX 324E
OR_COURSE = r'([A-Z]{2,6} [0-9]{3}[A-Z]? (OR|or) )+[A-Z]{2,6} [0-9]{3}[A-Z]?' # XXX 100 OR XXX 324E
COURSE_PATTERN = r'[A-Z]{2,6} [0-9]{3}[A-Z]?' # MATH 239A
CATEGORY_PATTERN = r'[0-9]{3}[A-Z]?' # 245R
SUBJECT_PATTERN = r'[A-Z]{2,6}' # MATH

ENG_OR_BRACKETS = r'(\(.+?\) or )+\(.+\)' # (XXX XXX) or (XXX XXX) or (XXX)

YEAR_PATTERN = r'[1-4](A|B)'

class ReplaceType(Enum):
    slash_category = 1
    slash_sub_comma_category = 2
    one_of_slash_sub_comma_category = 3
    slash_course = 4
    or_course = 5

class ParseResultIndicator(Enum):
    is_or = 1
    is_and = 2

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

    if re.search(r'(\(.+?\) or )+\(.+\)', prereq_string): # eng special (;) semi-colon inside brackets
        prereq_array = prereq_string.split('or \(')
        result_array = []
        for prereq_element in prereq_array:
            result_array.append(parse_course(prereq_element))
        return result_array

    prereq_dic = {}
    prereq_course = []
    prereq_year = []
    prereq_array = prereq_string.split(';')
    for prereq_element in prereq_array:
        if re.search(COURSE_PATTERN, prereq_element):
            prereq_course.append(parse_course(prereq_element))
        prereq_year.append(parse_year(prereq_element))

    prereq_dic['course'] = prereq_course
    prereq_dic['year'] = prereq_year

    return prereq_dic


def parse_year(input_year_string):

    input_year_string = re.sub(r'[0-9]{4}', '', input_year_string)
    return re.search(YEAR_PATTERN, input_year_string).group(0)

def parse_course(input_course_string):

    input_course_string = re.sub(r'[0-9]{4}', '', input_course_string)

    result_course_list = []

    replace_array = [] # index = course category - replace_num
    input_course_string = _course_replacer(input_course_string, replace_array)

    # Grab all the courses left.
    while re.search(COURSE_PATTERN, input_course_string):
        valid_course_string = re.search(COURSE_PATTERN, input_course_string).group(0)
        input_course_string = input_course_string.replace(valid_course_string, ' ', 1)

        if re.search(r'[0-9]{3}Z', valid_course_string):

            parsed_subject_name = re.search(SUBJECT_PATTERN, valid_course_string).group(0)
            parsed_category = re.search(CATEGORY_PATTERN, valid_course_string).group(0)
            course_parse_result = _course_dereplacer(parsed_subject_name, parsed_category, replace_array)
            if isinstance(course_parse_result, basestring):
                result_course_list.append(course_parse_result)

            elif re.search(COURSE_PATTERN, course_parse_result[0]):
                for course_string in course_parse_result:
                    result_course_list.append(course_string)
            else:
                course_slash_splitted_string = ''
                for category_string in course_parse_result:
                    if len(course_slash_splitted_string) > 0:
                        course_slash_splitted_string += '|'
                    course_slash_splitted_string += parsed_subject_name + ' ' + category_string

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
                    if len(result_string) > 0:
                        result_string += '|'

                    result_string += dereplace_result
                elif re.search(COURSE_PATTERN, dereplace_result[0]):
                    pass # considered not possible
                else:
                    subject_string = re.search(SUBJECT_PATTERN, searched_course).group(0)
                    for category_string in dereplace_result:
                        if len(result_string) > 0:
                            result_string += '|'
                        result_string += subject_string + ' ' + category_string
            else:
                if len(result_string) > 0:
                    result_string += '|'
                result_string += searched_course
        return result_string

    elif replace_type == ReplaceType.slash_sub_comma_category or \
        replace_type == ReplaceType.one_of_slash_sub_comma_category:

        result_string = ''
        result_list = []
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

        if replace_type == ReplaceType.one_of_slash_sub_comma_category:
            # used to indicate the affect range of 'one of'
            # result_string = str(len(searched_category_list)) + '|' + result_string
            for category_string in searched_category_list:
                if len(result_string) > 0:
                    result_string += '|'
                result_string += subject_string + ' ' + category_string
        else:
            for category_string in searched_category_list:
                result_list.append(subject_string + ' ' + category_string)

        return result_list

    elif replace_type == ReplaceType.slash_category:

        return _unwire_slash_category(replace_course_string)
    else:

        raise BaseException(202)


if __name__ == '__main__':
    # print parse_course('One of ECE 316, 318, Level at least 4A Computer Engineering or Electrical Engineering')
    # print parse_course('AAA 100, 200R, 300 or BBB 100/CCC 200, AMATH 242/341/CM 271/CS 371, DDD 111/222, EEE 111/222, RRR 100S')
    # print parse_course('CIVE 153 or (EARTH 121, 121L) or (level at least 3A Civil or Environmental or Geological Engineering) or (level at least 3A Earth Science/Hydrogeology Specialization)')
    # print re.search(CATEGORY_PATTERN, 'REP 103Z').group(0)
    print parse_course('CS 240, 241, 246, (CS 251 or ECE 222)')
