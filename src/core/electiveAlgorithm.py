
class ElectiveRecomender():
    def __init__(self, courses, liked_courses, disliked_courses, completed_courses, preferred_departments):
        self.courses = courses
        self.liked_courses = liked_courses # Courses that the user says they liked or would like to take
        self.disliked_courses = disliked_courses # Courses that the user says they disliked or would NOT like to take
        self.completed_courses = completed_courses # Courses that the user has completed & therefore cannot be recommended
        self.preferred_departments = preferred_departments