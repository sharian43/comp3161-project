# sec_disc.py
import re
from faker import Faker
import random
from insertscripts import write_sql

fake = Faker()

# Parse Course INSERT statements based on the updated table structure
def parse_courses(sql_file_path):
    courses = []
    pattern = r"INSERT INTO Course \(courseID, course_name, course_code, lecturerID, created_by\) VALUES \((\d+), '([^']+)', '(\w+)', (\d+), (\d+)\);"

    with open(sql_file_path, 'r') as file:
        for line in file:
            match = re.match(pattern, line)
            if match:
                course = {
                    "courseID": int(match.group(1)),
                    "course_name": match.group(2),
                    "course_code": match.group(3),
                    "lecturerID": int(match.group(4)),
                    "created_by": int(match.group(5))
                }
                courses.append(course)
    return courses

# Parse Student INSERT statements based on updated schema
def parse_students(sql_file_path):
    students = []
    pattern = r"INSERT INTO Student \(studentID, accountID, firstName, lastName, department, gpa\) VALUES \((\d+), (\d+), '[^']+', '[^']+', '[^']+', [\d.]+\);"

    with open(sql_file_path, 'r') as file:
        for line in file:
            match = re.match(pattern, line)
            if match:
                students.append({"student_id": int(match.group(1))})
    return students

# Generate Section INSERTs from parsed courses
def generate_sections(courses):
    sections = []
    for course in courses:
        section_id = course["courseID"]  # Simplified mapping
        section_name = f"{course['course_code']} - Section A"
        sections.append({
            "sectionID": section_id,
            "courseID": course["courseID"],
            "section_name": section_name
        })
    section_sql = [
        f"INSERT INTO Section (sectionID, courseID, section_name) VALUES "
        f"({s['sectionID']}, {s['courseID']}, '{s['section_name']}');"
        for s in sections
    ]
    return section_sql, sections

# Generate SectionItem INSERTs
def generate_section_items(sections):
    section_items = []
    item_sql = []
    item_id = 1
    for section in sections:
        for _ in range(random.randint(1, 3)):
            item_type = random.choice(["LECTURE_SLIDE", "ASSIGNMENT"])
            section_items.append({
                "itemID": item_id,
                "sectionID": section["sectionID"],
                "item_type": item_type
            })
            item_sql.append(
                f"INSERT INTO SectionItem (itemID, sectionID, item_type) VALUES "
                f"({item_id}, {section['sectionID']}, '{item_type}');"
            )
            item_id += 1
    return item_sql, section_items

# Generate LectureSlide INSERTs
def generate_lecture_slides(section_items):
    slide_sql = []
    for item in section_items:
        if item["item_type"] == "LECTURE_SLIDE":
            slide_name = f"Slide {random.randint(1, 10)} - {fake.word().capitalize()}"
            slide_sql.append(
                f"INSERT INTO LectureSlide (slideID, itemID, slide_name) VALUES "
                f"({item['itemID']}, {item['itemID']}, '{slide_name}');"
            )
    return slide_sql

# Generate Assignment INSERTs (no studentID or grade here due to schema update)
def generate_assignments(section_items):
    assignment_sql = []
    for item in section_items:
        if item["item_type"] == "ASSIGNMENT":
            assignment_name = f"{fake.word().capitalize()} Assignment"
            max_points = round(random.uniform(70, 100), 2)
            weight = round(random.uniform(0.5, 2.0), 2)
            assignment_sql.append(
                f"INSERT INTO Assignment (assignmentID, itemID, assignmentName, maxPoints, weight) VALUES "
                f"({item['itemID']}, {item['itemID']}, '{assignment_name}', {max_points}, {weight});"
            )
    return assignment_sql

# Generate DiscussionForum INSERTs
def generate_discussion_forums(courses, max_user_id):
    forum_sql = []
    forums = []
    for course in courses:
        topic = f"{fake.word().capitalize()} Discussion"
        creator_id = random.randint(1, max_user_id)
        forum_sql.append(
            f"INSERT INTO DiscussionForum (forumID, courseID, topic, creator) VALUES "
            f"({course['courseID']}, {course['courseID']}, '{topic}', {creator_id});"
        )
        forums.append({"forumID": course["courseID"], "creator": creator_id})
    return forum_sql, forums

# Generate DiscussionThread INSERTs with title and parent threading
def generate_discussion_threads(forums, max_user_id):
    thread_sql = []
    thread_id = 1
    for forum in forums:
        for _ in range(random.randint(3, 7)):
            user_id = random.randint(1, max_user_id)
            title = f"{fake.word().capitalize()} Topic"
            content = fake.paragraph(nb_sentences=3)
            thread_sql.append(
                f"INSERT INTO DiscussionThread (threadID, forumID, userID, title, content, parentThreadID) VALUES "
                f"({thread_id}, {forum['forumID']}, {user_id}, '{title}', '{content}', NULL);"
            )
            parent_id = thread_id
            thread_id += 1

            for _ in range(random.randint(1, 3)):
                user_id = random.randint(1, max_user_id)
                reply = fake.sentence()
                thread_sql.append(
                    f"INSERT INTO DiscussionThread (threadID, forumID, userID, title, content, parentThreadID) VALUES "
                    f"({thread_id}, {forum['forumID']}, {user_id}, NULL, '{reply}', {parent_id});"
                )
                thread_id += 1
    return thread_sql

# Main execution block (prevents accidental execution on import)
if __name__ == "__main__":
    courses = parse_courses("cms_course1.sql")
    students = parse_students("cms_student1.sql")
    max_user_id = len(students) + 100  # Assuming 100 lecturers

    section_sql, sections = generate_sections(courses)
    section_item_sql, section_items = generate_section_items(sections)
    slide_sql = generate_lecture_slides(section_items)
    assignment_sql = generate_assignments(section_items)
    forum_sql, forums = generate_discussion_forums(courses, max_user_id)
    thread_sql = generate_discussion_threads(forums, max_user_id)

    write_sql("cms_sections.sql", section_sql)
    write_sql("cms_section_items.sql", section_item_sql)
    write_sql("cms_slides.sql", slide_sql)
    write_sql("cms_assignments.sql", assignment_sql)
    write_sql("cms_forums.sql", forum_sql)
    write_sql("cms_threads.sql", thread_sql)

    print("Additional content files generated successfully.")
