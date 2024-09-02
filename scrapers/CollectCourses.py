import requests
import re
from bs4 import BeautifulSoup
import json

class CourseScraper():
    def main(self):
        page_number = 530 # The first page is page #0, this is not a bug
        page_exists = True
        courses = {}
        
        while page_exists:
            print(f'On page {page_number} of 532')
            url = f'https://www.mcgill.ca/study/2024-2025/courses/search?page={page_number}'
            soup = self.getSoup(url)
            found_courses = self.parseSoup(soup)
            if found_courses:
                for course in found_courses:
                    courses[course[0]] = course[1]
                
                page_number += 1
            else:
                page_exists = False # Looks like there are 532 pages

        with open('data/courses.json', 'w') as f:
            json.dump(courses, f, indent=4) 
            
    def getSoup(self, url):
        page_content = requests.get(url)
        soup = BeautifulSoup(page_content.content, 'html.parser')
        return soup
    
    def parseSoup(self, soup):
        courses = [] # (title, {info}) tuple
        courseElements = soup.find_all('div', class_='views-row')
        if len(courseElements) == 0:
            return None
        for course in courseElements:
            course_heading = course.find('h4', class_='field-content').get_text(strip=True)
            faculty = course.find('span', class_='views-field-field-faculty-code').get_text(strip=True)
            dept = course.find('span', class_='views-field-field-dept-code').get_text(strip=True)
            level = course.find('span', class_='views-field-level').get_text(strip=True)
            
            title = self.getTitle(course_heading)
            course_code = self.getCourseCode(course_heading)
            course_credits = self.getCredits(course_heading)
            
            course_info = {"faculty" : faculty,
                           "dept" : dept,
                           "level": level,
                           "course code": course_code,
                           "credits" : course_credits
                           }
            courses.append((title, course_info)) # appends a tuple which can later be added to our json file w/ the title as the key and the info as the value
            
            # print(f"Title: {title}")
            # print(f"Faculty: {faculty}")
            # print(f"Department: {dept}")
            # print(f"Level: {level}")
            # print(f"Code: {course_code}")
            # print(f"Credits: {course_credits}")
            # print("----------")
        
        return courses # ex. [('Intro to Coding', {info:info, info2:info2}), ...]
    
    def getTitle(self, course_heading):
        match = re.search(r'\d+\s(.*?)\s\(', course_heading)
        if match:
            return match.group(1).strip()
        return None
        
    def getCourseCode(self, title):
        # Gets the course code ex. COMP 202
        match = re.match(r'^[A-Z]+\s\d+', title)
        if match:
            return match.group()
        return None

    def getCredits(self, title):
        # Gets the course credits (int)
        match = re.search(r'\((\d+)\scredit', title)
        if match:
            return int(match.group(1))
        return None
        
if __name__ == '__main__':
    scraper = CourseScraper()
    scraper.main()