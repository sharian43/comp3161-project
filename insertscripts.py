from faker import Faker
import random
from datetime import datetime
import hashlib

Faker.seed(42)
random.seed(42)
fake = Faker()

departments = [
    "Mathematics", "Physics", "Chemistry", "Biology", "Economics", "Sociology",
    "Linguistics", "Psychology", "Philosophy", "Literature", "History", "Computing",
    "Journalism", "Accounts"
]
schedules = ["MWF 9-11", "TTH 10-12", "MW 1-3", "F 9-12", "TTH 3-5"]

NUM_STUDENTS =100000
NUM_LECTURERS = 95
NUM_ADMINS = 18
NUM_COURSES = 200

roles = {
    "STUDENT": NUM_STUDENTS,
    "LECTURER": NUM_LECTURERS,
    "ADMIN": NUM_ADMINS
}

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# Generate User data
def generate_users():
    user_data = []
    inserts = []

    for role, count in roles.items():
        for i in range(count):
            user_id = 1000 + len(user_data)
            username = fake.unique.user_name()
            raw_password = fake.password(length=12, special_chars=False)
            password = hash_password(raw_password)

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

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    total_users = len(user_data)

    unique_ids = random.sample(range(100, 1000000 + total_users), total_users)

    fake_first = fake.first_name
    fake_last = fake.last_name
    fake_email = fake.email
    fake_pass = fake.password
    sha_pass = hash_password

    for (user_id, username, role), account_id in zip(user_data, unique_ids):
        firstName = fake_first()
        lastName = fake_last()
        contact = fake_email()
        password = sha_pass(fake_pass(length=12, special_chars=False))

        accounts.append(
            f"INSERT INTO Account (accountID, userID, firstName, lastName, acc_contact_info, accRole, accPassword, created_at) "
            f"VALUES ({account_id}, {user_id}, '{firstName}', '{lastName}', '{contact}', '{role}', '{password}', '{now_str}');"
        )
        account_data.append((account_id, user_id, username, role, firstName, lastName))
    return accounts, account_data

# def generate_login_data(user_data):
#     return [
#         f"INSERT INTO Login (userID, session_period) VALUES ({user_id}, '{fake.date_this_year()}');"
#         for user_id, _, _ in user_data
#     ]

# Generate Admin data
def generate_admins(account_data):
    inserts = []
    admin_ids = []

    # Filter for ADMIN roles
    admin_accounts = [acc for acc in account_data if acc[3] == 'ADMIN']
    total_admins = len(admin_accounts)

    unique_admin_ids = random.sample(range(3000, 5001), total_admins)

    for (admin_id, (acc_id, user_id, username, role, first_name, last_name)) in zip(unique_admin_ids, admin_accounts):
        inserts.append(
            f"INSERT INTO Admin (adminID, accountID, firstName, lastName) "
            f"VALUES ({admin_id}, {acc_id}, '{first_name}', '{last_name}');"
        )
        admin_ids.append(admin_id)
    return inserts, admin_ids

# Generate Student data
def generate_students(account_data):
    inserts = []
    student_ids = []
    current_student_id = 620000000

    for acc_id, user_id, username, role, first_name, last_name in account_data:
        if role == 'STUDENT':
            dept = random.choice(departments)
            gpa = round(random.uniform(0.00, 4.0), 2)

            inserts.append(
                f"INSERT INTO Student (studentID, accountID, firstName, lastName, department, gpa) "
                f"VALUES ({current_student_id}, {acc_id}, '{first_name}', '{last_name}', '{dept}', {gpa});"
            )
            student_ids.append(current_student_id)
            current_student_id += 1
    return inserts, student_ids

# Generate Lecturer data
def generate_lecturers(account_data):
    lecturer_inserts = []
    lecturer_ids = []
    lecturer_accounts = [acc for acc in account_data if acc[3] == 'LECTURER']

    # Generate unique lecturer IDs starting from 7000
    start_id = 7000
    for i, (acc_id, user_id, username, role, first_name, last_name) in enumerate(lecturer_accounts):
        lec_id = start_id + i 

        dept = random.choice(departments)
        sched = random.choice(schedules)

        lecturer_inserts.append(
            f"INSERT INTO Lecturer (lecturerID, accountID, firstName, lastName, department, schedule) "
            f"VALUES ({lec_id}, {acc_id}, '{first_name}', '{last_name}', '{dept}', '{sched}');"
        )
        lecturer_ids.append(lec_id)
    return lecturer_inserts, lecturer_ids


def generate_courses(num_courses, lecturer_ids, admin_ids):
    courses = []
    lecturer_course_count = {lec_id: 0 for lec_id in lecturer_ids}

    course_ids = random.sample(range(1000, 10000), num_courses)

    course_codes = set()
    while len(course_codes) < num_courses:
        subject = random.choice(departments)
        prefix = subject[:4].upper()
        code = f"{prefix}{random.randint(100, 999)}"
        course_codes.add(code)
    course_codes = list(course_codes)

    for i in range(num_courses):
        subject = random.choice(departments)
        name = f"{random.choice(['Advanced', 'Introductory', 'Intermediate', 'Fundamentals of', 'Applied'])} {subject}"

        # Assign a lecturer with <5 courses
        eligible_lecturers = [lec for lec in lecturer_ids if lecturer_course_count[lec] < 5]
        if not eligible_lecturers:
            # If all lecturers have 5 courses, allow selecting any lecturer
            eligible_lecturers = lecturer_ids
        
        lecturer_id = random.choice(eligible_lecturers)
        lecturer_course_count[lecturer_id] += 1

        admin_id = random.choice(admin_ids)

        courses.append({
            "course_id": course_ids[i],
            "course_code": course_codes[i],
            "course_name": name,
            "lecturerID": lecturer_id,
            "created_by": admin_id
        })
    return courses

def generate_course_inserts(courses):
    return [
        f"INSERT INTO Course (courseID, course_name, course_code, lecturerID, created_by) "
        f"VALUES ({course['course_id']}, '{course['course_name']}', '{course['course_code']}', {course['lecturerID']}, {course['created_by']});"
        for course in courses
    ]
# Generate enrolments data
def generate_enrolments(student_ids, course_ids):
    enrolments = []
    course_enroll_count = {cid: 0 for cid in course_ids}
    student_course_map = {sid: set() for sid in student_ids}

    # assign 3 to 6 courses to each student
    for sid in student_ids:
        courses = random.sample(course_ids, k=random.randint(3, 6))
        student_course_map[sid] = set(courses)
        for cid in courses:
            enrolments.append(f"INSERT INTO Enrol (studentID, courseID) VALUES ({sid}, {cid});")
            course_enroll_count[cid] += 1

    under_enrolled = [cid for cid, count in course_enroll_count.items() if count < 10]
    for cid in under_enrolled:
        shortfall = 10 - course_enroll_count[cid]

        # find eligible students
        eligible = [sid for sid, enrolled in student_course_map.items() if cid not in enrolled and len(enrolled) < 6]

        if shortfall > len(eligible):
            shortfall = len(eligible)

        selected = random.sample(eligible, shortfall)
        for sid in selected:
            enrolments.append(f"INSERT INTO Enrol (studentID, courseID) VALUES ({sid}, {cid});")
            student_course_map[sid].add(cid)
            course_enroll_count[cid] += 1
    return enrolments

def write_sql(filename, statements, batch_size=10000):
    with open(filename, "w") as f:
        f.write("\n".join(statements))
        f.write("\n")

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
write_sql("cms_user1.sql", user_sql)
write_sql("cms_account1.sql", account_sql)
# write_sql("cms_login.sql", login_sql)
write_sql("cms_admin1.sql", admin_sql)
write_sql("cms_student1.sql", student_sql)
write_sql("cms_lecturer1.sql", lecturer_sql)
write_sql("cms_course1.sql", course_sql)
write_sql("cms_enrollment1.sql", enrol_sql)

print("All sql files generated successfully.")
