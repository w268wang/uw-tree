__author__ = 'wwang'

class CourseNode():
    def __init__(self, course_name):
        self.name = course_name
        self.pre_list = []
        self.next_list = []
        self.year = 1

    def add_pre(self, course_name):
        self.pre_list.append(course_name)

    def add_next(self, course_name):
        self.next_list.append(course_name)

    def set_year(self, year):
        self.year = year

    def get_name(self):
        return self.name

    def get_pre_list(self):
        return self.pre_list

    def get_next_list(self):
        return self.next_list

    def get_year(self):
        return self.year

    def can_take(self, taken_list):
        return set(taken_list).issubset(set(self.pre_list))