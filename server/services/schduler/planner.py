__author__ = 'wwang'

from ..common.course_node import CourseNode
from ..database import mongo
from ..util import course_render


def generate_plan(course_list):
    """

    :return:
    """


def _build_course_tree(course_list):
    course_node_dic = {}
    for course_name in course_list:
        course_node = CourseNode(course_name)
        course_info = mongo.get_course_by_name(course_name)
        course_prereq_list = []
        year_prereq = 1
        if len(course_info['teapot_prereq']) > 0:
            course_prereq_list = course_info['teapot_prereq']['course']
            year_prereq = course_info['teapot_prereq']['year']
        else:
            course_prereq_list = course_info['evaluated_prereq']['course']
            year_prereq = course_info['teapot_prereq']['year']

        course_node.set_year(course_render.year_to_number(year_prereq[0]))

        for prereq_course in course_prereq_list:
            course_node.add_pre(prereq_course)
            course_node_dic[prereq_course].add_next(prereq_course)

        course_node_dic[course_name] = (course_node)

def _get_start_point():
    pass
