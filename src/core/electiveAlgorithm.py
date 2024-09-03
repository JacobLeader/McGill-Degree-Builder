
import sys
 
# append the path of the
# parent directory
sys.path.append("..")

from utils.courseInfoHandler import getCourseLevel, getCourseInfo

class ElectiveRecomender():
    def __init__(self, courses, liked_courses, disliked_courses, completed_courses, preferred_departments):
        # All the lists of courses are dicts -> {title: {info:info, info2: info2, ...}, title: {...}}
        self.courses = courses
        self.liked_courses = liked_courses # Courses that the user says they liked or would like to take
        self.disliked_courses = disliked_courses # Courses that the user says they disliked or would NOT like to take
        self.completed_courses = completed_courses # Courses that the user has completed & therefore cannot be recommended
        self.preferred_departments = preferred_departments
        
    def recommend_course(self, year):
        # Algo can be changed!
        
        # If there is a user says they want to do an elective, they haven't done it yet, and the level is within a year, it seems straight forward to suggest it
        for course in self.liked_courses:
            course_info = getCourseInfo(course)
            course_level = int(getCourseLevel(course_info['course code'])[0]) #  1,2,3,4,5 or 6
            if course not in self.completed_courses and abs(year - course_level) <= 1:
                return course
            

            