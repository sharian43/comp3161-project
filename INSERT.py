from faker import Faker
import random

fake = Faker()

faculty = ["Humanities & Education", "Social Science", "Science & Technology"]
departments = ["Mathematics", "Physics", "Chemistry", "Biology", "Economics", "Sociology", "Linguistics",
               "Psychology", "Philosophy", "Literature", "History", "Computing", "Journalism", "Accounts"]

def generate_students(num_students):
    """Generates students with unique StudentIDs."""
    student_ids = set()
    students = []

    while len(student_ids) < num_students:
        student_id = random.randint(30000, 99999)
        if student_id not in student_ids: 
            student_ids.add(student_id)
            students.append({
                "student_id": student_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "Email": f"{student_id}_{fake.first_name().lower()}.{fake.last_name().lower()}@{fake.domain_name()}",
                "Address": fake.address(),
                "department": random.choice(departments),
                "Faculy": random.choice(faculty)
            })
    return students

def generate_lecturers(num_lecturers):
    """Generates unique lecturers."""
    lecturers = []
    lec_ids = set()

    while len(lecturers) < num_lecturers:
        lec_id = random.randint(1000, 9999)
        if lec_id not in lec_ids:
            lec_ids.add(lec_id)
            lecturers.append({
                "lec_id": lec_id,
                "name": fake.name(),
                "department": random.choice(departments),
                "Faculy": random.choice(faculty)
            })
    return lecturers

def generate_courses(num_courses, lecturers):
    """Generates courses with constraints on lecturers."""
    courses = []
    course_ids = set()
    lecturer_courses = {lecturer['lec_id']: 0 for lecturer in lecturers}  # Track courses per lecturer

    while len(courses) < num_courses:
        subject = random.choice(departments)
        subject_prefix = subject[:4].upper()

        # Ensure unique course IDs
        course_id = f"{random.randint(1000, 9999)}{subject_prefix}"
        if course_id not in course_ids:
            course_ids.add(course_id)

            course_name = f"{random.choice(['Advanced', 'Introductory', 'Intermediate', 'Fundamentals of', 'Applied', 'Introduction to'])} {subject}"

            # Assign a lecturer who has fewer than 5 courses
            available_lecturers = [lec for lec, count in lecturer_courses.items() if count < 5]
            if available_lecturers:
                lecturer_id = random.choice(available_lecturers)
                lecturer_courses[lecturer_id] += 1
            else:
                lecturer_id = random.choice(list(lecturer_courses.keys()))  # Reassign if all reached 5

            courses.append({
                "course_id": course_id,
                "course_name": course_name,
                "lec_id": lecturer_id
            })

    # Ensure each lecturer teaches at least 1 course
    for lecturer_id, count in lecturer_courses.items():
        if count == 0:
            subject = random.choice(departments)
            subject_prefix = subject[:4].upper()
            course_id = f"{random.randint(1000, 9999)}{subject_prefix}"
            course_name = f"{random.choice(['Advanced', 'Introductory', 'Intermediate', 'Fundamentals of', 'Applied', 'Introduction to'])} {subject}"
            lecturer_courses[lecturer_id] += 1
            courses.append({
                "course_id": course_id,
                "course_name": course_name,
                "lec_id": lecturer_id
            })

    return courses

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
            grade = random.randint(0, 100)

            enrollments.append({
                "student_id": student["student_id"],
                "course_id": course["course_id"],
                "grade": grade
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
                    "grade": random.randint(0, 100)
                })

    return enrollments

num_students = 100000
num_lecturers = 50
num_courses = 200

students = generate_students(num_students)
lecturers = generate_lecturers(num_lecturers)
courses = generate_courses(num_courses, lecturers)
enrollments = generate_enrollments(students, courses)

sql_file = "3161proj.sql"

with open(sql_file, "w") as f:
    for student in students:
        f.write(f"INSERT INTO Student (StudentID, FirstName, LastName) VALUES ({student['student_id']}, '{student['first_name']}', '{student['last_name']}');\n")

    for lec in lecturers:
        f.write(f"INSERT INTO Lecturer (LecID, LecName, Department) VALUES ({lec['lec_id']}, '{lec['name']}', '{lec['department']}');\n")

    for course in courses:
        f.write(f"INSERT INTO Course (CourseID, CourseName, LecID) VALUES ({course['course_id']}, '{course['course_name']}', {course['lec_id']});\n")
    
    for enroll in enrollments:
        f.write(f"INSERT INTO Enrollment (StudentID, CourseID, Grade) VALUES ({enroll['student_id']}, {enroll['course_id']}, {enroll['grade']});\n")

print(f"SQL file '{sql_file}' generated successfully!")   