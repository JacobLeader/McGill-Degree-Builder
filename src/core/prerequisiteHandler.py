

class PrerequisiteCheck():
    def __init__(self, completed_courses=[], courses_scheduled=[]):
        self.completed_courses = completed_courses
        self.courses_scheduled = courses_scheduled # Courses that will be taken by the time the prerequisites are needed
        
    def hasPrerequisites(self, course):
        # TODO
        return True