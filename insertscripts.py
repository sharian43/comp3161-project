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
schedules = ["MWF 9-11", "TTH 10-12", "MW 1-3", "F 9-12", "TTH 3-5"]

NUM_STUDENTS =100600
NUM_LECTURERS = 93
NUM_ADMINS = 13
NUM_COURSES = 195

roles = {
    "STUDENT": NUM_STUDENTS,
    "LECTURER": NUM_LECTURERS,
    "ADMIN": NUM_ADMINS
}

# Generate User data
def generate_users():
    user_data = []
    inserts = []
    used_user_ids = set()
    used_usernames = set()

    for role, count in roles.items():
        if role in ["STUDENT", "LECTURER", "ADMIN"]:
            for _ in range(count):
                user_id = 1000 + len(used_user_ids)
                used_user_ids.add(user_id)


                while True:
                    username = fake.user_name()
                    if username not in used_usernames:
                        used_usernames.add(username)
                        break
                password = hash_password(fake.password(length=12), length=64)
                inserts.append(
                    f"INSERT INTO User (userID, username, userPassword) "
                    f"VALUES ({user_id}, '{username}', '{password}');"
                )
                user_data.append((user_id, username, role))
    return inserts, user_data

# Generate Account data
def generate_account_data(user_data):
    accounts = []
    account_data = []
    account_ids = set()

    for user_id, username, role in user_data:
        firstName = fake.first_name()
        lastName = fake.last_name()
        contact = fake.email()
        password = hash_password(fake.password(length=12), length=64)
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
        account_id = random.randint(1000, 9999)
        while account_id in account_ids:
            account_id = random.randint(1000, 9999)
        account_ids.add(account_id)

        accounts.append(
            f"INSERT INTO Account (accountID, userID, firstName, lastName, acc_contact_info, accRole, accPassword, created_at) "
            f"VALUES ({account_id}, {user_id}, '{firstName}', '{lastName}', '{contact}', '{role}', '{password}', '{created_at}');"
        )

        account_data.append((account_id, user_id, username, role, firstName, lastName))
    return accounts, account_data

def hash_password(pw, length = 10):
    hashed_pw = hashlib.sha256(pw.encode()).hexdigest() 
    return hashed_pw[:length]

# def generate_login_data(user_data):
#     return [
#         f"INSERT INTO Login (userID, session_period) VALUES ({user_id}, '{fake.date_this_year()}');"
#         for user_id, _, _ in user_data
#     ]

# Generate Admin data
def generate_admins(account_data):
    inserts = []
    admin_ids = []
    used_ids = set()

    for acc_id, user_id, username, role, first_name, last_name in account_data:
        if role == 'ADMIN':
            admin_id = random.randint(3000, 5000)
            while admin_id in used_ids:
                admin_id = random.randint(3000, 5000)
            used_ids.add(admin_id)

            inserts.append(
                f"INSERT INTO Admin (adminID, accountID, firstName, lastName) VALUES ({admin_id}, {acc_id}, '{first_name}', '{last_name}');"
            )
            admin_ids.append(admin_id)
    return inserts, admin_ids

# Generate Student data
def generate_students(account_data):
    inserts = []
    student_ids = []
    used_ids = set()

    for acc_id, user_id, username, role, first_name, last_name in account_data:
        if role == 'STUDENT':
            student_id = random.randint(100000, 999999)
            while student_id in used_ids:
                student_id = random.randint(100000, 999999)
            used_ids.add(student_id)

            dept = random.choice(departments)
            gpa = round(random.uniform(0.00, 4.0), 2)

            inserts.append(
                f"INSERT INTO Student (studentID, accountID, firstName, lastName, department, gpa) VALUES ({student_id}, {acc_id}, '{first_name}', '{last_name}', '{dept}', {gpa});"
            )
            student_ids.append(student_id)
    return inserts, student_ids

# Generate Lecturer data
def generate_lecturers(account_data):
    lecturer_inserts = []
    lecturer_ids = []
    used_ids = set()

    for acc_id, user_id, username, role, first_name, last_name in account_data:
        if role == 'LECTURER':
            lec_id = random.randint(1000, 9999)
            while lec_id in used_ids:
                lec_id = random.randint(1000, 9999)
            used_ids.add(lec_id)

            dept = random.choice(departments)
            sched = random.choice(schedules)

            lecturer_inserts.append(
                f"INSERT INTO Lecturer (lecturerID, accountID, firstName, lastName, department, schedule) VALUES ({lec_id}, {acc_id}, '{first_name}', '{last_name}', '{dept}', '{sched}');"
            )
            lecturer_ids.append(lec_id)
    return lecturer_inserts, lecturer_ids

def generate_courses(num_courses, lecturer_ids, admin_ids):
    """Generates course data for insertion into the Course table."""
    courses = []
    course_codes = set()
    course_ids = set()

    for _ in range(num_courses):
        subject = random.choice(departments)
        prefix = subject[:4].upper()
        code = f"{prefix}{random.randint(100, 999)}"
        cid = random.randint(1000, 9999)

        while cid in course_ids:
            cid = random.randint(1000, 9999)
        while code in course_codes:
            code = f"{prefix}{random.randint(100, 999)}"

        course_ids.add(cid)
        course_codes.add(code)

        name = f"{random.choice(['Advanced', 'Introductory', 'Intermediate', 'Fundamentals of', 'Applied'])} {subject}"
        lecturer_id = random.choice(lecturer_ids)
        admin_id = random.choice(admin_ids)

        courses.append({"course_id": cid, "course_code": code, "course_name": name, "lecturerID": lecturer_id, "created_by": admin_id})
    return courses

def generate_course_inserts(courses):
    return [
        f"INSERT INTO Course (courseID, course_name, course_code, lecturerID, created_by) VALUES ({c['course_id']}, '{c['course_name']}', '{c['course_code']}', {c['lecturerID']}, {c['created_by']});"
        for c in courses
    ]

# Generate enrolments data
def generate_enrolments(student_ids, course_ids):
    enrolments = []
    course_enroll_count = {cid: 0 for cid in course_ids}
    student_course_map = {}

    for sid in student_ids:
        courses = random.sample(course_ids, k=random.randint(3, 6))
        student_course_map[sid] = set(courses)
        for cid in courses:
            enrolments.append(f"INSERT INTO Enrol (studentID, courseID) VALUES ({sid}, {cid});")
            course_enroll_count[cid] += 1

    for cid, count in course_enroll_count.items():
        if count < 10:
            shortfall = 10 - count
            eligible = [sid for sid in student_ids if cid not in student_course_map[sid] and len(student_course_map[sid]) < 6]
            selected = random.sample(eligible, k=shortfall)
            for sid in selected:
                enrolments.append(f"INSERT INTO Enrol (studentID, courseID) VALUES ({sid}, {cid});")
                student_course_map[sid].add(cid)
    return enrolments


def write_sql(filename, statements, batch_size=1000):
    with open(filename, "w") as f:
        for i in range(0, len(statements), batch_size):
            f.write("\n".join(statements[i:i + batch_size]) + "\n")


user_sql, user_data = generate_users()
account_sql, account_data = generate_account_data(user_data)
# login_sql = generate_login_data(user_data)
admin_sql, admin_pairs = generate_admins(account_data)
student_sql, student_ids = generate_students(account_data)
lecturer_sql, lecturer_ids = generate_lecturers(account_data)
courses = generate_courses(NUM_COURSES, lecturer_ids, admin_pairs)
course_sql = generate_course_inserts(courses)
course_ids = [c["course_id"] for c in courses]
enrol_sql = generate_enrolments(student_ids, course_ids)

# Save to files
write_sql("cms_user.sql", user_sql)
write_sql("cms_account.sql", account_sql)
# write_sql("cms_login.sql", login_sql)
write_sql("cms_admin.sql", admin_sql)
write_sql("cms_student.sql", student_sql)
write_sql("cms_lecturer.sql", lecturer_sql)
write_sql("cms_course.sql", course_sql)
write_sql("cms_enrollment.sql", enrol_sql)

print("All sql files generated successfully.")
