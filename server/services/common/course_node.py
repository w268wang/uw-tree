__author__ = 'wwang'

class CourseNode():
    def __init__(self, course_name, valid = True):

        # Represents the course this node represents
        self.name = course_name

        # list of lists of course name
        self.pre_list = []

        # list of next possible course after taking this course
        self.next_list = []

        # the year restriction of the current course
        self.year = 1

        self.valid = valid

    def setAsValid(self):
        self.valid = True

    def add_pre(self, course_name):
        self.pre_list.append(course_name.split('|'))

    def add_next(self, course_name):
        self.next_list.append(course_name)

    def set_year(self, year):
        self.year = year

    def can_take(self, taken_list):
        for course_item in self.pre_list:
            has_taken = False
            for course_name in course_item:
                if course_name in taken_list:
                    has_taken = True
                    break
            if not has_taken:
                return False
        print 'yes'
        return True

if __name__ == '__main__':
    node = CourseNode('a')
    node.add_pre('CS 146|CS 136|CS 138')
    print node.pre_list
    node.can_take([])