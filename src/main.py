
from utils.courseLoader import loadCourseData
import pprint

class Main():
    def __init__(self):
        self.courses = loadCourseData()
        
if __name__ == '__main__':
    main = Main()
    