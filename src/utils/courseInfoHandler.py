import re
from utils.courseLoader import loadCourseData
import json

# class CourseInfo():
#     def __init__(self):
courses = loadCourseData()
    
def getCourseInfo(course_title):
    return courses[course_title]
    
def getCourseCode(course_code):
    match = re.search(r'\d+$', course_code) # \d+ means more then one digit, $ means its at the end of the string
    if match:
        return match.group(0)
    
def extractCourseTitle(text):
    # "COMP 251 Algorithms and Data Structures (3 credits)" -> "Algorithms and Data Structures"
    match = re.search(r'\d+\s(.*?)\s\(', text)
    if match:
        return match.group(1).strip()
    return None
    
def getMajorInfo(major):
    file_name_ending = major.replace(" ", "_")
    file_path = f"data/major_{file_name_ending}.json"
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
    
def isSimilarCourse(course1: str, course2: str):
    # TODO: ex. deductive logic 1 vs deductive logic 2
    ...