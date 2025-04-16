from faker import Faker
import random
from datetime import datetime
import hashlib

fake = Faker()

departments = [
    "Mathematics", "Physics", "Chemistry", "Biology", "Economics", "Sociology",
    "Linguistics", "Psychology", "Philosophy", "Literature", "History", "Computing",
    "Journalism", "Accounts"
]

schedule = ["MWF 9-11", "TTH 10-12", "MW 1-3", "F 9-12", "TTH 3-5"]

NUM_STUDENTS = 100100
NUM_LECTURERS = 100
NUM_ADMINS = 5
NUM_COURSES = 220

roles = {
    "STUDENT": NUM_STUDENTS,
    "LECTURER": NUM_LECTURERS,
    "ADMIN": NUM_ADMINS
}

def generate_account_data():
    accounts, data, used_names = [], [], set()
    current_id = 1

    for role, count in roles.items():
        for _ in range(count):
            while True:
                acc_name = fake.user_name()
                if acc_name not in used_names:
                    used_names.add(acc_name)
                    break
            contact = fake.email()
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            accounts.append(f"INSERT INTO Account (acc_name, acc_contact_info, accRole, created_at) "
                            f"VALUES ('{acc_name}', '{contact}', '{role}', '{created_at}');")
            data.append((current_id, acc_name, role))
            current_id += 1
    return accounts, data

def hash_password(pw, length = 10):
    hashed_pw = hashlib.sha256(pw.encode()).hexdigest() 
    return hashed_pw[:length]

def generate_users(account_data):
    inserts = []
    for acc_id, acc_name, role in account_data:
        if role in ["STUDENT", "LECTURER"]:
            username = acc_name if random.random() > 0.5 else fake.user_name()
            hashed = hash_password(fake.password(length=12))
            inserts.append(f"INSERT INTO User (accountID, username, userPassword) "
                           f"VALUES ({acc_id}, '{username}', '{hashed}');")
    return inserts

def generate_admins(account_data):
    return [
        f"INSERT INTO Admin (accountID, firstName, lastName) VALUES "
        f"({acc_id}, '{fake.first_name()}', '{fake.last_name()}');"
        for acc_id, _, role in account_data if role == 'ADMIN'
    ]

def generate_lecturers(account_data):
    lecturers, inserts = [], []
    lecturer_id = 1 
    for acc_id, _, role in account_data:
        if role == 'LECTURER':
            fname, lname = fake.first_name(), fake.last_name()
            dept = random.choice(departments)
            sched = random.choice(schedule)
            inserts.append(f"INSERT INTO Lecturer (lecturerID, accountID, firstName, lastName, department, schedule) "
                           f"VALUES ({lecturer_id}, {acc_id}, '{fname}', '{lname}', '{dept}', '{sched}');")
            lecturers.append({'lecturerID': lecturer_id, 'accountID': acc_id})
            lecturer_id += 1
    return inserts, lecturers

def generate_students(account_data):
    inserts, students = [], []
    for acc_id, _, role in account_data:
        if role == 'STUDENT':
            fname, lname = fake.first_name(), fake.last_name()
            dept = random.choice(departments)
            gpa = round(random.uniform(1.0, 4.0), 2)
            inserts.append(f"INSERT INTO Student (accountID, firstName, lastName, department, gpa) "
                           f"VALUES ({acc_id}, '{fname}', '{lname}', '{dept}', {gpa});")
            students.append({'student_id': acc_id})
    return inserts, students

def generate_courses(num_courses, lecturers):
    courses = []
    course_codes = set()
    course_ids = set()
    lec_course_count = {lec['lecturerID']: 0 for lec in lecturers}

    for _ in range(num_courses):
        available_lecs = [lec for lec in lecturers if lec_course_count[lec['lecturerID']] < 5]
        if not available_lecs:
            break
        subject = random.choice(departments)
        prefix = subject[:4].upper()
        courseID = random.randint(1000, 9999)
        while courseID in course_ids:
            courseID = random.randint(1000, 9999)
        code = f"{prefix}{random.randint(100, 999)}"
        while code in course_codes:
            code = f"{prefix}{random.randint(100, 999)}"

        lecturer = random.choice(available_lecs)
        lec_course_count[lecturer['lecturerID']] += 1

        courses.append({
            "courseID": courseID,
            "course_code": code,
            "course_name": f"{random.choice(['Intro', 'Advanced', 'Fundamentals of'])} {subject}",
            "lecturerID": lecturer['lecturerID'],
            "created_by": random.randint(1, NUM_ADMINS)
        })
    return courses

def generate_enrollments(students, courses):
    enrollments = []
    course_enroll_count = {course['courseID']: 0 for course in courses}
    for student in students:
        selected = random.sample(courses, random.randint(3, 6))
        for course in selected:
            enrollments.append(f"INSERT INTO Enrollment (StudentID, CourseID) VALUES ({student['student_id']}, {course['courseID']});")
            course_enroll_count[course['courseID']] += 1

    for courseID, count in course_enroll_count.items():
        if count < 10:
            to_add = 10 - count
            for _ in range(to_add):
                student = random.choice(students)
                enrollments.append(f"INSERT INTO Enrol (StudentID, CourseID) VALUES ({student['student_id']}, {courseID});")

    return enrollments

def write_sql(filename, statements):
    with open(filename, "w") as f:
        f.write("\n".join(statements))

account_sql, account_data = generate_account_data()
user_sql = generate_users(account_data)
admin_sql = generate_admins(account_data)
lecturer_sql, lecturers = generate_lecturers(account_data)
student_sql, students = generate_students(account_data)
courses = generate_courses(NUM_COURSES, lecturers)
course_sql = [f"INSERT INTO Course (courseID, course_code, course_name, lecturerID, created_by) "
              f"VALUES ({c['courseID']}, '{c['course_code']}', '{c['course_name']}', {c['lecturerID']}, {c['created_by']});"
              for c in courses]
enrollment_sql = generate_enrollments(students, courses)

# Save to files
write_sql("cms_accounts.sql", account_sql)
write_sql("cms_users.sql", user_sql)
write_sql("cms_admins.sql", admin_sql)
write_sql("cms_lecturers.sql", lecturer_sql)
write_sql("cms_students.sql", student_sql)
write_sql("cms_courses.sql", course_sql)
write_sql("cms_enrollments.sql", enrollment_sql)

print("All sql files generated successfully.")
