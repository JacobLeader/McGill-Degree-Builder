import sys
sys.path.append("..") # append the path of the parent directory to allow access to sibling directories
from utils.courseInfoHandler import getMajorInfo, extractCourseTitle, getCourseCode, getCourseInfo
from core.prerequisiteHandler import PrerequisiteCheck

class CoreRecommender:
    def __init__(self, liked_courses, disliked_courses, completed_courses, scheduled_courses, major):
        self.liked_courses = liked_courses
        self.disliked_courses = disliked_courses
        self.completed_courses = completed_courses
        self.scheduled_courses = scheduled_courses
        self.major = major
        self.major_info = getMajorInfo(major)
        
    def recommendCoreCourse(self, year):
        required_courses = self.major_info["Required Courses"]
        complementary_courses = self.major_info["Complementary Courses"]
        
        for course in required_courses:
            course_title = extractCourseTitle(course)
            course_info = getCourseInfo(course)
            course_level = getCourseCode(course_info["course code"])[0]
            
            # If the required course is an appropriate level & has not been completed
            if abs(course_level - year) >= 1 and course_title not in self.completed_courses + self.scheduled_courses:
                return course_title
            
            