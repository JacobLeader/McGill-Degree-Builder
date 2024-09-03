import re
from utils.courseLoader import loadCourseData

# class CourseInfo():
#     def __init__(self):
courses = loadCourseData()
    
def getCourseInfo(course_title):
    return courses[course_title]
    
def getCourseCode(course_code):
    match = re.search(r'\d+$', course_code) # \d+ means more then one digit, $ means its at the end of the string
    if match:
        return match.group(0)
    