__author__ = 'wwang'

from server.services.common.course_node import CourseNode
from server.services.database import mongo
from server.services.util import course_render


def generate_plan(course_list):
    """
    Returns a possible course plan based on given course list.
    :param course_list: A list of course names to generate plan.
    :return: A array of length 8 representing the course plan generated.
    """
    course_node_dic = _build_course_tree(course_list)

    plan_result = []
    taken_course_list = []

    start_courses = _get_start_point(course_node_dic)
    plan_result.append(start_courses)
    taken_course_list.extend(start_courses)

    remained_course_list = list(course_node_dic.keys())
    term_num = 1
    while len(remained_course_list) > 0:
        has_change = False
        term_course_list = []

        for remained_course in remained_course_list:
            if course_node_dic[remained_course].can_take(taken_course_list):
                has_change = True
                term_course_list.append(remained_course)
                taken_course_list.append(remained_course)

        if not has_change:
            return plan_result, remained_course_list
        plan_result.append(term_course_list)

        remained_course_list = filter(lambda name : name not in term_course_list, remained_course_list)
        term_num += 1

    return plan_result, []

def _build_course_tree(course_list):
    course_node_dic = {}
    for course_name in course_list:
        if course_name not in course_node_dic.keys():
            course_node = CourseNode(course_name)
        else:
            course_node = course_node_dic[course_name]
            course_node.setAsValid()

        course_info = mongo.get_course_by_name(course_name)
        course_prereq_list = []
        year_prereq = '1A'

        # Retrieve prereq info from db
        if len(course_info.teapot_prereq) > 0:
            course_prereq_list = course_info.teapot_prereq['course']
            if 'year' in course_info.teapot_prereq:
                year_prereq = course_info.teapot_prereq['year'][0]
        elif len(course_info.evaluated_prereq) > 0:
            course_prereq_list = course_info.evaluated_prereq['course']
            if 'year' in course_info.teapot_prereq:
                year_prereq = course_info.teapot_prereq['year'][0]
        # Set prereq year info to the course node
        course_node.set_year(course_render.year_to_number(year_prereq))

        if len(course_prereq_list) > 0 and isinstance(course_prereq_list[0], list):
            course_prereq_list = course_prereq_list[0]

        # Update the existing
        for prereq_course in course_prereq_list:
            prereq_course_parts = prereq_course.split('|')
            for prereq_course_part in prereq_course_parts:
                if prereq_course_part not in course_node_dic.keys():
                    course_node_dic[prereq_course_part] = CourseNode(prereq_course_part, valid = False)
                course_node_dic[prereq_course_part].add_next(course_name)
            course_node.add_pre(prereq_course)

        course_node_dic[course_name] = course_node
    return _clean_dic(course_node_dic)

def _get_start_point(course_node_dic):
    """
    Finds the start courses and build the plan gradually.
    Uses the idea of BFS.
    :param course_node_list:
    :return:
    """
    start_course_list = []
    for course_name, course_node in course_node_dic.iteritems():
        if 0 == len(course_node.pre_list):
            start_course_list.append(course_name)

    for course_name in start_course_list:
        del course_node_dic[course_name]

    return start_course_list

def _filter_by_name(name, name_list):
    return name in name_list

def _clean_dic(dic):
    delete_course_name_list = []
    for course_name, course_node in dic.iteritems():
        if not course_node.valid:
            delete_course_name_list.append(course_name)
    for course_name in delete_course_name_list:
        del dic[course_name]

    return dic

def _get_course_prereq_list(course_list):
    prereq_info_dic = {}
    for course_name in course_list:
        course_info = mongo.get_course_by_name(course_name)
        course_prereq_list = []

        # Retrieve prereq info from db
        if len(course_info.teapot_prereq) > 0:
            course_prereq_list = course_info.teapot_prereq['course']
        elif len(course_info.evaluated_prereq) > 0:
            course_prereq_list = course_info.evaluated_prereq['course']

        prereq_info_dic[course_name] = course_prereq_list

    return prereq_info_dic

if __name__ == '__main__':
    print generate_plan(['CS 135', 'CS 146', 'CS 246', 'CS 245', 'MATH 135'])