
import sys
sys.path.append("..") # append the path of the parent directory to allow access to sibling directories
from utils.courseInfoHandler import getCourseCode, getCourseInfo
from utils.courseLoader import loadCourseData
from core.prerequisiteHandler import PrerequisiteCheck

class ElectiveRecommender():
    def __init__(self, courses, liked_courses, disliked_courses, completed_courses, preferred_departments):
        # All the lists of courses are dicts -> {title: {info:info, info2: info2, ...}, title: {...}}
        self.courses = courses
        self.liked_courses = liked_courses # Courses that the user says they liked or would like to take
        self.disliked_courses = disliked_courses # Courses that the user says they disliked or would NOT like to take
        self.completed_courses = completed_courses # Courses that the user has completed & therefore cannot be recommended
        self.preferred_departments = preferred_departments
        
    def recommend_course(self, year):
        prerequisite_checker = PrerequisiteCheck(self.completed_courses, [])
        # Algo can be changed!
        
        # If there is a user says they want to do an elective, they haven't done it yet, and the level is within a year, it seems straight forward to suggest it
        for course in self.liked_courses:
            course_info = getCourseInfo(course)
            course_level = int(getCourseCode(course_info['course code'])[0]) #  1,2,3,4,5 or 6
            if course not in self.completed_courses and abs(year - course_level) <= 1 and prerequisite_checker.hasPrerequisites(course):
                return course
            
        courses_data = loadCourseData()
        for course_title in courses_data.keys():
            try:
                course_info = courses_data[course_title]
                valid_course = True
                course_level = int(getCourseCode(course_info['course code'])[0]) #  1,2,3,4,5 or 6
                
                for course in self.completed_courses + self.disliked_courses: # check if the course is in either completed or disliked courses
                    #! more logic is needed here to avoid recommending similar courses to those that are disliked, ex. deductive logic 1 & deductive logic 2
                    course_code = getCourseInfo(course)['course code']
                    if course_code == course_info['course code']:
                        valid_course = False
                        continue
                    
                if valid_course and course_info['dept'] in self.preferred_departments and abs(year - course_level) <= 1 and prerequisite_checker.hasPrerequisites(course):
                    return course_title
            except:
                pass
                

            