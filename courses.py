from faker import Faker
import random

fake = Faker()

departments = [
    "Mathematics", "Physics", "Chemistry", "Biology", "Economics", "Sociology", "Linguistics",
    "Psychology", "Philosophy", "Literature", "History", "Computing", "Journalism", "Accounts"
]

schedule = ["MWF 9-11", "TTH 10-12", "MW 1-3", "F 9-12", "TTH 3-5"]

def generate_lecturers(num_lecturers):
    """Generates unique lecturers."""
    lecturers = []
    lec_ids = set()

    while len(lecturers) < num_lecturers:
        lec_id = random.randint(1000, 9999)
        user_id = random.randint(100, 999) 
        if lec_id not in lec_ids:
            lec_ids.add(lec_id)
            name = fake.name()

            lecturers.append({
                "lec_id": lec_id,
                "user_id": user_id,
                "name": name,
                "department": random.choice(departments),
                "schedule": random.choice(schedule)
            })
    return lecturers

def generate_courses(num_courses, lecturers):
    courses = []
    course_codes = set()
    course_ids = set()
    lecturer_course_count = {lec['lec_id']: 0 for lec in lecturers}

    for _ in range(num_courses):
        available_lecturers = [lec for lec in lecturers if lecturer_course_count[lec['lec_id']] < 5]
        if not available_lecturers:
            break  # No more lecturers to assign

        subject = random.choice(departments)
        subject_prefix = subject[:4].upper()
        course_code = f"{subject_prefix}{random.randint(100, 999)}"
        course_num = random.randint(1000, 9999)

        while course_num in course_ids:
            course_num = random.randint(1000, 9999)
        while course_code in course_codes:
            course_code = f"{subject_prefix}{random.randint(100, 999)}"

        lecturer = random.choice(available_lecturers)
        lecturer_course_count[lecturer['lec_id']] += 1

        courses.append({
            "course_id": course_num,
            "course_code": course_code,
            "course_name": f"{random.choice(['Advanced', 'Introductory', 'Intermediate', 'Fundamentals of', 'Applied'])} {subject}",
            "lecturerID": lecturer["lec_id"],
            "created_by": random.randint(1, 5)
        })

        course_codes.add(course_code)
        course_ids.add(course_num)

    return courses


def generate_students(num_students):
    """Generates students with unique StudentIDs."""
    student_ids = set()
    students = []

    while len(student_ids) < num_students:
        student_id = random.randint(30000, 99999)
        userID = random.randint(1000, 99999)
        if student_id not in student_ids:  # Ensure uniqueness
            student_ids.add(student_id)
            students.append({
                "student_id": student_id,
                "userID": userID,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "department": random.choice(departments),
                "gpa": round(random.uniform(1.0, 4.0), 2)
            })
    return students

def generate_enrollments(students, courses):
    """Generate enrollments ensuring valid CourseIDs and constraints."""
    enrollments = []
    student_courses = {student['student_id']: [] for student in students}  # Track courses per student
    course_students = {course['course_id']: 0 for course in courses}  # Track students per course

    for student in students:
        # Ensure each student is enrolled in at least 3 and no more than 6 courses
        num_courses = random.randint(3, 6)
        chosen_courses = random.sample(courses, num_courses)  # Select courses for this student

        for course in chosen_courses:

            enrollments.append({
                "student_id": student["student_id"],
                "course_id": course["course_id"],
            })

            student_courses[student["student_id"]].append(course["course_id"])
            course_students[course["course_id"]] += 1

    # Ensure each course has at least 10 students
    for course_id, count in course_students.items():
        if count < 10:
            deficit = 10 - count
            # Randomly add students to meet the requirement
            for _ in range(deficit):
                student = random.choice(students)
                enrollments.append({
                    "student_id": student["student_id"],
                    "course_id": course_id,
                })
    return enrollments


# Generate 
num_lecturers = 100
lecturers = generate_lecturers(num_lecturers)

num_courses = 210
courses = generate_courses(num_courses, lecturers)

num_students = 50020
students = generate_students(num_students)

enrollments = generate_enrollments(students, courses)

# Save lecturers and courses to SQL files
lecturer_sql_file = "cms_lecturers.sql"
course_sql_file = "cms_courses.sql"
enrollment_sql_file = "cms_enrollment.sql"
student_sql_file_1 = "cms_students_part1.sql"
student_sql_file_2 = "cms_students_part2.sql"

with open(lecturer_sql_file, "w") as f:
    for lecturer in lecturers:
        f.write(f"INSERT INTO Lecturer (lecturerID, userID, Name, department, schedule) VALUES "
                f"({lecturer['lec_id']}, {random.randint(100, 999)}, '{lecturer['name']}', "
                f"'{lecturer['department']}', '{lecturer['schedule']}');\n")

with open(course_sql_file, "w") as f:
    for course in courses:
        f.write(f"INSERT INTO Course (course_id, course_code, course_name, lecturerID, created_by) "
                f"VALUES ('{course['course_id']}','{course['course_code']}', '{course['course_name']}', {course['lecturerID']}, {course['created_by']});\n")

with open(enrollment_sql_file, "w") as f:
    for enroll in enrollments:
        f.write(f"INSERT INTO Enrollment (StudentID, CourseID) VALUES ({enroll['student_id']}, {enroll['course_id']});\n")

# Write first half to part1
with open(student_sql_file_1, "w") as f1:
    for student in students:
        f1.write(
            f"INSERT INTO Student (StudentID, FirstName, LastName, department, gpa) "
            f"VALUES ({student['student_id']}, '{student['first_name']}', '{student['last_name']}', "
            f"'{student['department']}', '{student['gpa']}');\n"
        )

with open(student_sql_file_2, "w") as f2:
    for student in students:
        f2.write(
            f"INSERT INTO Student (StudentID, FirstName, LastName, department, gpa) "
            f"VALUES ({student['student_id']}, '{student['first_name']}', '{student['last_name']}', "
            f"'{student['department']}', '{student['gpa']}');\n"
        )

print(f"SQL files '{lecturer_sql_file}', '{course_sql_file}', '{enrollment_sql_file}', '{student_sql_file_1}', '{student_sql_file_2}'generated successfully!")
