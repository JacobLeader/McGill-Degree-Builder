# This following code is to scrape the mcgill website to extract all the possible major and minors
import requests
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import json

class DegreeScraper():
    # def __init__(self):
    #     self.url = 'https://www.mcgill.ca/study/2024-2025/faculties/arts/undergraduate/programs/bachelor-arts-ba-major-concentration-computer-science#ba_csi8_major_ar'
        
    def getSoup(self, url):
        page_content = requests.get(url)
        soup = BeautifulSoup(page_content.content, 'html.parser')
        return soup
    
    # Return [str], {str:[str]}
    def separateCourseTypes(self, soup):
        required_courses = []
        complementary_courses = defaultdict(list) # default dict is better here because if the group key hasnt been created it creates a new one with a list as the value
        
        headings = soup.find_all('h4') # Things like "Required Courses (18 credits)" and "Complementary Courses (18 credits)" are h4 headings 
        
        for heading in headings:
            heading_text = heading.get_text(strip=True)
            
            if 'Required Courses' in heading_text:
                course_set = heading.find_next('ul', class_='program-set') # Find the next list of courses (course set)
                if course_set:
                    courses = course_set.find_all('li', class_='program-course') # Each course has a list item tag (li)
                    for course_item in courses:
                        course_title = course_item.find('a', class_='program-course-title') # The course title is a hyperlink (a)
                        if course_title:
                            required_courses.append(self.clean_string(course_title.get_text(strip=True)))
            
            elif 'Complementary Courses' in heading_text:
                current_element = heading.next_sibling
                while current_element:
                    if isinstance(current_element, str): # Pass over linebreak elements etc. 
                        current_element = current_element.next_sibling
                        continue

                    # Finds the lists of courses aka the "groups"
                    if current_element.name == 'ul' and 'program-set' in current_element.get('class', []):
                        group_heading = current_element.find_previous('p') # right when we find a list of courses we look above for the closest text, we know this will be the group name
                        group_letter = 'Unknown'
                        if group_heading:

                            match = re.search(r'(Group|List)\s+([A-Z])', group_heading.get_text(strip=True)) # "Group" or "List" then a space(\s+) then an upper case letter ([A-Z])
                            if match:
                                group_letter = match.group(2) # Gets the ex. 'A' part of the match
                        
                        courses = current_element.find_all('li', class_='program-course') # Gets the list items from the set, these are the course elements
                        for course_item in courses:
                            course_title = course_item.find('a', class_='program-course-title') # the course title is the hyperlink (a) part of the list item element
                            if course_title:
                                complementary_courses[group_letter].append(self.clean_string(course_title.get_text(strip=True)))
                    
                    current_element = current_element.next_sibling

        return required_courses, dict(complementary_courses)
    
    def clean_string(self, course):
        # Define the unwanted patterns
        unwanted_patterns = [
            r'\*',      # Asterisks
            r'\r',      # Carriage returns
            r'\s{2,}'   # Multiple spaces
        ]
        
        # Remove unwanted patterns
        for pattern in unwanted_patterns:
            course = re.sub(pattern, '', course)
        
        # Trim leading and trailing whitespace
        return course.strip()
        
if __name__ == '__main__':
    scraper = DegreeScraper()
    url = 'https://www.mcgill.ca/study/2024-2025/faculties/arts/undergraduate/programs/bachelor-arts-ba-major-concentration-computer-science#ba_csi8_major_ar'
    soup = scraper.getSoup(url)
    required_courses, complementary_courses = scraper.separateCourseTypes(soup)
    
    degree = {
        "Required Courses" : required_courses,
        "Complementary Courses" : complementary_courses
    }
        
    with open('data/CS_Major.json', 'w') as f:
        json.dump(degree, f, indent=4)
        
        
        
        
        
        


'''
EXAMPLE OUTPUT (JSON):
    {
        "program": {
            "name": "Major Concentration Philosophy",
            "totalCredits": 36,
            "department": "Philosophy",
            "degree": "Bachelor of Arts",
            "requirements": {
            "requiredCourses": [
                {
                "courseCode": "PHIL 210",
                "courseName": "Introduction to Deductive Logic 1",
                "credits": 3
                }
            ],
            "complementaryCourses": {
                "totalCredits": 33,
                "restrictions": {
                "max200": 9, <- Max 200 level credits (9)
                "min400/500": 9
                },
                "creditDistribution": [
                {
                    "credits": 18,
                    "groups": [
                    { "group": "A", "credits": 3 },
                    { "group": "B", "credits": 3 },
                    { "group": "C/D", "credits": 6 },
                    { "group": "E", "credits": 3 },
                    { "group": "F", "credits": 3 }
                    ]
                },
                {
                    "credits": 15,
                    "description": "Additional credits from Groups A, B, C, D, E, F, or other PHIL courses. Only one of PHIL 200 or PHIL 201 may be included."
                }
                ]
            }
            },
            "groups": {
            "A": [
                { "courseCode": "PHIL 306", "courseName": "Philosophy of Mind", "credits": 3 },
                { "courseCode": "PHIL 310", "courseName": "Intermediate Logic", "credits": 3 },
                { "courseCode": "PHIL 311", "courseName": "Philosophy of Mathematics", "credits": 3 },
                { "courseCode": "PHIL 341", "courseName": "Philosophy of Science 1", "credits": 3 },
                { "courseCode": "PHIL 411", "courseName": "Topics in Philosophy of Logic and Mathematics", "credits": 3 },
                { "courseCode": "PHIL 415", "courseName": "Philosophy of Language", "credits": 3 },
                { "courseCode": "PHIL 419", "courseName": "Epistemology", "credits": 3 },
                { "courseCode": "PHIL 421", "courseName": "Metaphysics", "credits": 3 },
                { "courseCode": "PHIL 441", "courseName": "Philosophy of Science 2", "credits": 3 },
                { "courseCode": "PHIL 470", "courseName": "Topics in Contemporary Analytic Philosophy", "credits": 3 }
            ],
            "B": [
                { "courseCode": "PHIL 375", "courseName": "Existentialism", "credits": 3 },
                { "courseCode": "PHIL 474", "courseName": "Phenomenology", "credits": 3 },
                { "courseCode": "PHIL 475", "courseName": "Topics in Contemporary European Philosophy", "credits": 3 }
            ],
            "C": [
                { "courseCode": "PHIL 344", "courseName": "Medieval and Renaissance Political Theory", "credits": 3 },
                { "courseCode": "PHIL 345", "courseName": "Greek Political Theory", "credits": 3 },
                { "courseCode": "PHIL 350", "courseName": "History and Philosophy of Ancient Science", "credits": 3 },
                { "courseCode": "PHIL 353", "courseName": "The Presocratic Philosophers", "credits": 3 },
                { "courseCode": "PHIL 354", "courseName": "Plato", "credits": 3 },
                { "courseCode": "PHIL 355", "courseName": "Aristotle", "credits": 3 },
                { "courseCode": "PHIL 356", "courseName": "Early Medieval Philosophy", "credits": 3 },
                { "courseCode": "PHIL 452", "courseName": "Later Greek Philosophy", "credits": 3 },
                { "courseCode": "PHIL 453", "courseName": "Ancient Metaphysics and Natural Philosophy", "credits": 3 },
                { "courseCode": "PHIL 454", "courseName": "Ancient Moral Theory", "credits": 3 }
            ],
            "D": [
                { "courseCode": "PHIL 360", "courseName": "17th Century Philosophy", "credits": 3 },
                { "courseCode": "PHIL 361", "courseName": "18th Century Philosophy", "credits": 3 },
                { "courseCode": "PHIL 366", "courseName": "18th and Early 19th Century German Philosophy", "credits": 3 },
                { "courseCode": "PHIL 367", "courseName": "19th Century Philosophy", "credits": 3 },
                { "courseCode": "PHIL 444", "courseName": "Early Modern Political Theory", "credits": 3 },
                { "courseCode": "PHIL 445", "courseName": "19th Century Political Theory", "credits": 3 }
            ],
            "E": [
                { "courseCode": "PHIL 230", "courseName": "Introduction to Moral Philosophy 1", "credits": 3 },
                { "courseCode": "PHIL 237", "courseName": "Contemporary Moral Issues", "credits": 3 },
                { "courseCode": "PHIL 240", "courseName": "Political Philosophy 1", "credits": 3 },
                { "courseCode": "PHIL 242", "courseName": "Introduction to Feminist Theory", "credits": 3 }
            ],
            "F": [
                { "courseCode": "PHIL 334", "courseName": "Ethical Theory", "credits": 3 },
                { "courseCode": "PHIL 343", "courseName": "Biomedical Ethics", "credits": 3 },
                { "courseCode": "PHIL 348", "courseName": "Philosophy of Law 1", "credits": 3 },
                { "courseCode": "PHIL 427", "courseName": "Topics in Critical Philosophy of Race", "credits": 3 },
                { "courseCode": "PHIL 434", "courseName": "Metaethics", "credits": 3 },
                { "courseCode": "PHIL 442", "courseName": "Topics in Feminist Theory", "credits": 3 }
            ]
            }
        }
    }
'''