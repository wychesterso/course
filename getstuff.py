import requests
from bs4 import BeautifulSoup
import csv


def get_course_info(course_code):
    
    course_url = f'https://programs-courses.uq.edu.au/course.html?course_code={course_code}'

    response = requests.get(course_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    course_level = soup.find('p', {'id': 'course-level'}).text.strip() if soup.find('p', {'id': 'course-level'}) else None
    
    course_faculty = soup.find('p', {'id': 'course-faculty'}).text.strip() if soup.find('p', {'id': 'course-faculty'}) else None
    
    course_units = soup.find('p', {'id': 'course-units'}).text.strip() if soup.find('p', {'id': 'course-units'}) else None
    
    course_duration = soup.find('p', {'id': 'course-duration'}).text.strip() if soup.find('p', {'id': 'course-duration'}) else None
    
    course_incompatible = soup.find('p', {'id': 'course-incompatible'}).text.strip() if soup.find('p', {'id': 'course-incompatible'}) else None
    
    course_prerequisite = soup.find('p', {'id': 'course-prerequisite'}).text.strip() if soup.find('p', {'id': 'course-prerequisite'}) else None
    
    course_recommended_prerequisite = soup.find('p', {'id': 'course-recommended-prerequisite'}).text.strip() if soup.find('p', {'id': 'course-recommended-prerequisite'}) else None
    
    return {
        'Course Level': course_level,
        'Faculty': course_faculty,
        'Units': course_units,
        'Duration': course_duration,
        'Incompatible Courses': course_incompatible,
        'Prerequisites': course_prerequisite,
        'Recommended Prerequisites': course_recommended_prerequisite
    }


def get_course_offerings(course_code):
    
    course_url = f'https://programs-courses.uq.edu.au/course.html?course_code={course_code}'

    response = requests.get(course_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    offerings = []
    offering_rows = soup.find_all('tr', {'id': lambda x: x and x.startswith('course-offering')})
    
    for row in offering_rows:
        
        semester = row.find('a', {'class': 'course-offering-year'}).text.strip() if row.find('a', {'class': 'course-offering-year'}) else None
        semester = semester.split('(')[0].strip()  # remove date
        
        location = row.find('td', {'class': 'course-offering-location'}).text.strip() if row.find('td', {'class': 'course-offering-location'}) else None
        mode = row.find('td', {'class': 'course-offering-mode'}).text.strip() if row.find('td', {'class': 'course-offering-mode'}) else None
        
        offerings.append((semester, location, mode))
    
    return offerings




path = str(input("Enter path: "))
    
while (True):
    
    search_term = str(input("Enter search term: "))
    
    if search_term == "q":
        break


    url = f'https://programs-courses.uq.edu.au/search.html?keywords={search_term}&searchType=coursecode&archived=true&CourseParameters%5Bsemester%5D='

    response = requests.get(url)

    # check if the request was successful
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # find all course list items
        courses = soup.find_all('li')

        with open(fr'{path}\courses.csv', 'w', newline='', encoding='utf-8') as course_file:
            writer = csv.writer(course_file)

            for course in courses:
                
                # extract course code
                course_code_tag = course.find('a', class_='code')
                course_code = course_code_tag.text.strip() if course_code_tag else None

                # extract course title
                course_title_tag = course.find('a', class_='title')
                course_title = course_title_tag.text.strip() if course_title_tag else None

                # write only if both code and title exist
                if course_code and course_title:
                    course_info = get_course_info(course_code)
                    writer.writerow([
                        course_code, course_title, 
                        course_info.get('Course Level'), 
                        course_info.get('Faculty'),
                        course_info.get('Units'), 
                        course_info.get('Duration'),
                        course_info.get('Incompatible Courses'), 
                        course_info.get('Prerequisites'),
                        course_info.get('Recommended Prerequisites')
                    ])

    else:
        print(response.status_code)   
        



    valid_semesters = ["Summer Semester, 2024", "Semester 1, 2025", "Semester 2, 2025"]



    with open(fr'{path}\courses.csv', 'r', newline='', encoding='utf-8') as course_file:
        
        reader = csv.reader(course_file)
        
        with open(fr'{path}\offerings.csv', 'w', newline='', encoding='utf-8') as offering_file:
            writer = csv.writer(offering_file)
            
            for row in reader:
                course_code = row[0]
                offerings = get_course_offerings(course_code)
                
                for offering in offerings:
                    semester = offering[0]
                    
                    if semester in valid_semesters:
                        writer.writerow([course_code, offering[0], offering[1], offering[2]])