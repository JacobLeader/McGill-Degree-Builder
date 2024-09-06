
from utils.courseLoader import loadCourseData
from core.electiveAlgorithm import ElectiveRecommender
from core.coreCourseAlgorithm import CoreRecommender
import pprint

class Main():
    def __init__(self):
        self.courses = loadCourseData()
        self.scheduled_courses = []
        
    def getElectives(self):
        liked_courses = [
            # "Introduction to Artificial Intelligence Ethics",
            # "Mechanics and Waves"
        ]

        disliked_courses = [
            "Introduction to Deductive Logic 1",
            "Economic Botany"
        ]

        completed_courses = [
            "Introductory Physics - Electromagnetism",
            "Mechanics Laboratory"
        ]

        preferred_departments = [
            "Physics",
            "Philosophy"
        ]
        major = "Computer Science"
        
        elective_recommender = ElectiveRecommender(self.courses, liked_courses, disliked_courses, completed_courses, preferred_departments)
        recommended_elective = elective_recommender.recommend_course(1)
        self.scheduled_courses.append(recommended_elective)
        print(recommended_elective)
        
        core_recommender = CoreRecommender(self.courses, liked_courses, disliked_courses, completed_courses, self.scheduled_courses, major)
        recommended_core_course = core_recommender.recommendCoreCourse(1)
        self.scheduled_courses.append(recommended_core_course)
        
if __name__ == '__main__':
    main = Main()
    main.getElectives()
    