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
    course_node_list = _build_course_tree(course_list)

    plan_result = []
    taken_course_list = []

    start_courses = _get_start_point(course_node_list)
    plan_result[0] = start_courses
    taken_course_list.extend(start_courses)

    remained_course_list = list(course_node_list)

    term_num = 1
    while len(remained_course_list) > 0:
        term_course_list = []
        for remained_course in remained_course_list:
            if remained_course.can_take(taken_course_list):
                term_course_list.append(remained_course)

        plan_result[term_num] = term_course_list
        remained_course_list.remove(term_course_list)
        term_num += 1

    return plan_result

def _build_course_tree(course_list):
    course_node_dic = {}
    for course_name in course_list:
        course_node = CourseNode(course_name)
        course_info = mongo.get_course_by_name(course_name)
        course_prereq_list = []
        year_prereq = '1A'

        # Retrieve prereq info from db
        if len(course_info.teapot_prereq) > 0:
            course_prereq_list = course_info.teapot_prereq.course
            year_prereq = course_info.teapot_prereq['year'][0]
        elif len(course_info.evaluated_prereq) > 0:
            course_prereq_list = course_info.evaluated_prereq['course']
            if 'year' in course_info.teapot_prereq:
                year_prereq = course_info.teapot_prereq['year'][0]

        # Set prereq year info to the course node
        course_node.set_year(course_render.year_to_number(year_prereq))

        # Update the existing
        for prereq_course in course_prereq_list:

            if not prereq_course in course_node_dic:
                course_node_dic[prereq_course] = CourseNode(prereq_course)

            course_node.add_pre(course_node_dic[prereq_course])
            course_node_dic[prereq_course].add_next(course_node)

        course_node_dic[course_name] = course_node
    return course_node_dic.values()

def _get_start_point(course_node_list):
    """
    Finds the start courses and build the plan gradually.
    Uses the idea of BFS.
    :param course_node_list:
    :return:
    """
    start_course_list = []
    for course_node in course_node_list:
        if 0 == len(course_node.get_pre_list()):
            start_course_list.append(course_node.get_name())

    return start_course_list

if __name__ == '__main__':
    generate_plan(['CS 135', 'CS 136', 'CS 246', 'CS 245'])