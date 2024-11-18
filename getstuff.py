import requests
from bs4 import BeautifulSoup
import csv

url = 'https://programs-courses.uq.edu.au/search.html?keywords=&searchType=coursecode&archived=true&CourseParameters%5Bsemester%5D='

response = requests.get(url)

# check if the request was successful
if response.status_code == 200:
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # find all course list items
    courses = soup.find_all('li')

    with open(r'C:\Users\Chester So\Documents\-_-\Python Stuff\courses.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for course in courses:
            # extract course code
            course_code_tag = course.find('a', class_='code')
            course_code = course_code_tag.text.strip() if course_code_tag else None

            # extract course title
            course_title_tag = course.find('a', class_='title')
            course_title = course_title_tag.text.strip() if course_title_tag else None

            # write only if both code and title exist
            if course_code and course_title:
                writer.writerow([course_code, course_title])

else:
    print(response.status_code)