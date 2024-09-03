import requests
import re
from bs4 import BeautifulSoup
import json

class CourseScraper():
    def main(self):
        page_number = 0 # The first page is page #0, this is not a bug
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
            course_link = course.find('h4', class_='field-content').find('a')['href'] # Gets the heading, which has a hyperlink (a tag) to the course page
            course_link = "https://www.mcgill.ca/" + course_link
            faculty = course.find('span', class_='views-field-field-faculty-code').get_text(strip=True)
            dept = course.find('span', class_='views-field-field-dept-code').get_text(strip=True)
            level = course.find('span', class_='views-field-level').get_text(strip=True)
            
            description, prerequisites, corequisites = self.parseCoursePage(course_link)
            title = self.getTitle(course_heading)
            course_code = self.getCourseCode(course_heading)
            course_credits = self.getCredits(course_heading)
            
            course_info = {"faculty" : faculty,
                           "dept" : dept,
                           "level" : level,
                           "course code" : course_code,
                           "credits" : course_credits,
                           "description" : description,
                           "prerequisites" : prerequisites,
                           "corequisites" : corequisites
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
    
    def parseCoursePage(self, course_link):
        soup = self.getSoup(course_link)
        description = self.getDescription(soup)
        prerequisites = self.getPrerequisites(soup) 
        corequisites = self.getCorequisites(soup)

        return description, prerequisites, corequisites

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
    
    def getDescription(self, soup):
        overview_header = soup.find('h3', text='Overview') # Find where it says overview

        description_element = overview_header.find_next_sibling('p') # find the closest paragraph tag, this is always the description
        description = description_element.get_text(strip=True)
        return description
        
    def getPrerequisites(self, soup):
        '''
        Use a sublist for when given 'or' in prereqs (would use a tuple, but json does not support tuples)
        Ex. Prerequisites: MATH 235 and either (MATH 247 or MATH 251).
        -> ['Math 235', ['MATH 247', 'MATH 251']]
        Ex. Prerequisites: MATH 247 or MATH 251 or equivalent, and MATH 248 or MATH 358 or equivalent, MATH 325.
        -> [['MATH 247', 'MATH 251'], ['MATH 248', 'MATH 358'], 'MATH 325']
        Ex. Prerequisites: MATH 222, MATH 247 or MATH 251, MATH 255 or permission of the Department.
        -> ['MATH 222', ['MATH 247', 'MATH 251'], ['MATH 255', 'permision of the Department']]
        '''
        notes_section = soup.find('ul', 'catalog-notes')
        if notes_section:
            paragraph_elements = notes_section.findAll('p')

            for paragraph_element in paragraph_elements:
                text = paragraph_element.get_text()
                if 'Prerequisite' in text:
                    text = text.strip("Prerequisite: ")
                    text = text.strip("(s): ")
                    prereqs = []
                    
                    prereqs_chunked = text.split(', ') # chunked by commas
                    prereqs_chunked = [prereq.strip() for prereq in prereqs_chunked]
                    
                    for chunk in prereqs_chunked:
                        and_chunks = chunk.split('and') # Cant think of a better variable name for this
                        for and_chunk in and_chunks:
                            if 'or' in and_chunk:
                                prereqs.append(tuple(and_chunk.split(' or ')))
                                    
                            # elif 'and' in chunk: 
                            #     prereqs.extend(chunk) # Split these up, so we extend the list
                            else:
                                prereqs.append(and_chunk)
                    
                    # prereqs = re.split(r'\s+or\s+|\s+and\s+|,\s*|\.\s*', text) # Split by "or", "and", ","
                    # prereqs = [req.strip() for req in prereqs if req.strip()] # remove whitespace & empty items
                    return prereqs
        return []
        
    def getCorequisites(self, soup):
        notes_section = soup.find('ul', 'catalog-notes')
        if notes_section:
            paragraph_elements = notes_section.findAll('p')
            for paragraph_element in paragraph_elements:
                text = paragraph_element.get_text()
                if 'Corequisite' in text:
                    text = text.strip("Corequisite: ")
                    text = text.strip("(s): ")
                    coreq = re.split(r'\s+or\s+|\s+and\s+|,\s*|\.\s*', text) # Split by "or", "and", ","
                    coreq = [req.strip() for req in coreq if req.strip()] # remove whitespace & empty items
                    return coreq
        return []
    
if __name__ == '__main__':
    scraper = CourseScraper()
    scraper.main()