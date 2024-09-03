
from utils.courseLoader import loadCourseData
from core.electiveAlgorithm import ElectiveRecommender
import pprint

class Main():
    def __init__(self):
        self.courses = loadCourseData()
        self.courses_scheduled = []
        
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
        
        elective_recommender = ElectiveRecommender(self.courses, liked_courses, disliked_courses, completed_courses, preferred_departments)
        print(elective_recommender.recommend_course(1))
        
        
if __name__ == '__main__':
    main = Main()
    main.getElectives()
    