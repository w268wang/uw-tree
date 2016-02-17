__author__ = 'wwang'

import mongoengine as mongo

class Course(mongo.Document):

    ###################
    # Data calculated #
    ###################

    # The full course code for this course
    # subject + ' ' + category e.g. CS 246
    name = mongo.StringField(primary_key = True, required = True)

    # Computer readable prerequisites info evaluated by parser
    evaluated_prereq = mongo.ListField(required = True)

    # Computer readable prerequisites info evaluated by a teapot
    teapot_prereq = mongo.ListField(required = False)


    ##################################
    # Data provided by uwaterloo api #
    ##################################

    # The digit id assigned to the course. e.g. 004380
    course_id = mongo.StringField(required = True)

    # The subject of the course. e.g. CS
    subject = mongo.StringField(required = True)

    # The category of the course. e.g. 246
    category = mongo.StringField(required = True)

    # The title of the course. e.g. Object-Oriented Software Development
    title = mongo.StringField(required = True)

    # The unit you can gain by finishing the course. e.g. 0.5
    units = mongo.DecimalField(required = True)

    # The course description. e.g. Introduction to object-oriented...
    description = mongo.StringField(required = False)

    # The activities may be involved in this course. e.g. ["LAB", "LEC", "TST", "TUT"]
    instructions = mongo.ListField(required = False)

    # The requirement you need to satisfy to enroll this course. e.g. CS 145 taken fall...
    prerequisites = mongo.StringField(required = False)

    # The antirequisite info of this course. e.g. SYDE 322
    antirequisites = mongo.StringField(required = False)

    # The corequisite info of this course.
    corequisites = mongo.StringField(required = False)

    # The crosslisting info of this course.
    crosslistings = mongo.StringField(required = False)

    # The terms our school offer this course. e.g. ["F", "W"]
    terms_offered = mongo.ListField(required = False)

    # The note of this course. e.g. [Note: Enrolment is restricted; ...
    notes = mongo.StringField(required = False)

    # The availibility info of this course. e.g. ["online":false, "online_only":false, ...
    offerings = mongo.DictField(required = False)

    # The needs_department_consent info.
    needs_department_consent = mongo.BooleanField(required = False)

    # The needs_instructor_consent info.
    needs_instructor_consent = mongo.BooleanField(required = False)

    # Some extra info.
    extra = mongo.ListField(required = False)

    # The calendar year of this course. e.g. 1516
    calendar_year = mongo.StringField(required = False)

    # The url of this course. e.g. http:\/\/www.ucalendar.uwaterloo.ca\/1516\/COURSE\/course-CS.html#CS246
    url = mongo.StringField(required = False)

    # The academic_level info of this course. e.g. undergraduate
    academic_level = mongo.StringField(required = False)

    # TODO fields
    # keywords: words extract from the course
    #

