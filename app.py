from flask import Flask, jsonify, request, redirect, url_for, session
import mysql.connector
import json
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('secret_key')

db = mysql.connector.connect(host='localhost', user=os.getenv('DB_User'), password= os.getenv('DB_Password'), database='cms')

cursor = db.cursor(dictionary=True)


@app.route('/register/user', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    userPassword = data.get('userPassword')

    if not all([username, userPassword]): 
        return jsonify({'error': 'Missing required fields'}), 400

    hashed_password = generate_password_hash(userPassword)

    try:
        cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({'error': 'User already exists'}), 409

        cursor.execute(
            "INSERT INTO User (username, userPassword) VALUES (%s, %s)",
            (username, hashed_password)
        )

        db.commit()
        return jsonify({'message': 'registered successfully'}), 201

    except Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/register/account/student', methods=['POST'])
def register_student_account():

    data = request.get_json()
    username = data.get('username')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    acc_contact_info = data.get('acc_contact_info')
    department = data.get('department')
    accPassword = data.get('accPassword')

    if not all([username, firstName, lastName, acc_contact_info, department, accPassword]):
        return jsonify({'error': 'Missing fields'}), 400

    hashed_password = generate_password_hash(accPassword)

    accRole = 'STUDENT'

    try:
        cursor.execute("SELECT userID FROM User WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'User not found'}), 404
        userID = user['userID']
        
        cursor.execute("SELECT * FROM Account WHERE userID = %s", (userID,))
        if cursor.fetchone():
            return jsonify({'error': 'Account already exists'}), 409

        cursor.execute("INSERT INTO Account (userID, firstName, lastName, acc_contact_info, accRole, accPassword) VALUES (%s, %s, %s, %s, %s, %s)", 
        (userID, firstName, lastName, acc_contact_info, accRole, hashed_password,))

        cursor.execute("SELECT LAST_INSERT_ID()")
        accountID = cursor.fetchone()['LAST_INSERT_ID()']

        gpa = 0.00
        cursor.execute(
            "INSERT INTO Student (accountID, firstName, lastName, department, gpa) VALUES (%s, %s, %s, %s, %s)",
            (accountID, firstName, lastName, department, gpa)
        )

        db.commit()

        return jsonify({'message': 'Account created successfully'}), 201

    except Error as e:
        return jsonify({'error': str(e)}), 500



@app.route('/register/account/lecturer', methods=['POST'])
def register_lecturer_account():

    data = request.get_json()
    username = data.get('username')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    acc_contact_info = data.get('acc_contact_info')
    department = data.get('department')
    accPassword = data.get('accPassword')

    if not all([username, firstName, lastName, acc_contact_info, department, accPassword]):
        return jsonify({'error': 'Missing fields'}), 400

    hashed_password = generate_password_hash(accPassword)

    accRole = 'LECTURER'

    try:
        cursor.execute("SELECT userID FROM User WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'User not found'}), 404
        userID = user['userID']
        
        cursor.execute("SELECT * FROM Account WHERE userID = %s", (userID,))
        if cursor.fetchone():
            return jsonify({'error': 'Account already exists'}), 409

        cursor.execute("INSERT INTO Account (userID, firstName, lastName, acc_contact_info, accRole, accPassword) VALUES (%s, %s, %s, %s, %s, %s)", 
        (userID, firstName, lastName, acc_contact_info, accRole, hashed_password,))

        cursor.execute("SELECT LAST_INSERT_ID()")
        accountID = cursor.fetchone()['LAST_INSERT_ID()']

        schedule = None
        cursor.execute(
            "INSERT INTO Lecturer (accountID, firstName, lastName, department, schedule) VALUES (%s, %s, %s, %s, %s)",
            (accountID, firstName, lastName, department, schedule)
        )

        db.commit()

        return jsonify({'message': 'Account created successfully'}), 201

    except Error as e:
        return jsonify({'error': str(e)}), 500



@app.route('/register/account/admin', methods=['POST'])
def register_admin_account():

    data = request.get_json()
    username = data.get('username')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    acc_contact_info = data.get('acc_contact_info')
    accPassword = data.get('accPassword')

    if not all([username, firstName, lastName, acc_contact_info, accPassword]):
        return jsonify({'error': 'Missing fields'}), 400

    hashed_password = generate_password_hash(accPassword)

    accRole = 'ADMIN'

    try:
        cursor.execute("SELECT userID FROM User WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'User not found'}), 404
        userID = user['userID']
        
        cursor.execute("SELECT * FROM Account WHERE userID = %s", (userID,))
        if cursor.fetchone():
            return jsonify({'error': 'Account already exists'}), 409

        cursor.execute("INSERT INTO Account (userID, firstName, lastName, acc_contact_info, accRole, accPassword) VALUES (%s, %s, %s, %s, %s, %s)", 
        (userID, firstName, lastName, acc_contact_info, accRole, hashed_password,))

        cursor.execute("SELECT LAST_INSERT_ID()")
        accountID = cursor.fetchone()['LAST_INSERT_ID()']

        cursor.execute(
            "INSERT INTO Admin (accountID, firstName, lastName) VALUES (%s, %s, %s)",
            (accountID, firstName, lastName)
        )
        db.commit()

        return jsonify({'message': 'Account created successfully'}), 201

    except Error as e:
        return jsonify({'error': str(e)}), 500



@app.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data.get('username')
    userPassword = data.get('userPassword')

    if not all([username, userPassword]):
        return jsonify({'error': 'Missing login credentials'}), 400

    try:

        cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user['userPassword'], userPassword):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        userID = user['userID']

        cursor.execute("SELECT * FROM Account WHERE userID = %s", (userID,))
        account = cursor.fetchone()

        accRole = account['accRole']

        if accRole not in ['STUDENT', 'LECTURER', 'ADMIN']:
            return jsonify({'error': 'Cannot login'}), 403

        cursor.execute("INSERT INTO Login (userID) VALUES (%s)", (userID,))
        db.commit()
        
        session['userID'] = user['userID']
        session['accRole'] = account['accRole']

        return jsonify({'message': 'Login successful', 'Role': accRole}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500



@app.route('/courses/create-course', methods=['POST'])
def create_course():
    data = request.get_json()
    course_name = data.get('course_name')
    course_code = data.get('course_code')
    lecturerID = data.get('lecturerID')


    if not all([course_name, course_code, lecturerID]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:

        userID = session['userID']

        cursor.execute("SELECT * FROM Account WHERE userID = %s", (userID,))
        account = cursor.fetchone()
        accRole = account['accRole']
        if accRole not in ['ADMIN']:
            return jsonify({'error': 'Access denied. Only admins can create courses.'}), 403
        
        accountID = account['accountID']

        cursor.execute('SELECT * from Admin WHERE accountID = %s', (accountID,))
        admin = cursor.fetchone()

        created_by = admin['adminID']

        cursor.execute("SELECT * FROM Lecturer WHERE lecturerID = %s", (lecturerID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Lecturer not identified'}), 400

        cursor.execute("SELECT * FROM Course WHERE course_code = %s", (course_code,))
        if cursor.fetchone():
            return jsonify({'error': 'Course already exists'}), 409

        cursor.execute(
            """INSERT INTO `Course` (course_name, course_code, lecturerID, created_by) VALUES (%s, %s, %s, %s)""",
            (course_name, course_code, lecturerID, created_by))
        db.commit()

        return jsonify({'message': 'Course created successfully'}), 201

    except Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/courses/retrieve-courses', methods=['POST'])
def retrieve_courses():
    data = request.get_json()

    studentID = data.get('studentID')
    lecturerID = data.get('lecturerID')

    try:

        # Case 1: Get all courses
        if not studentID and not lecturerID:
            cursor.execute("SELECT * FROM Course")
            courses = cursor.fetchall()
            return jsonify({'All Courses': courses}), 200

        # Case 2: Get courses for a particular student
        if studentID:
            cursor.execute("""
                SELECT c.courseID, c.course_name, c.lecturerID
                FROM Course c
                JOIN Enrol r ON c.CourseID = r.CourseID
                WHERE r.StudentID = %s
            """, (studentID,))
            courses = cursor.fetchall()
            return jsonify({'All Student courses': courses}), 200

        # Case 3: Get courses taught by a particular lecturer
        if lecturerID:
            cursor.execute("""
                SELECT courseID, course_name
                FROM Course
                WHERE lecturerID = %s
            """, (lecturerID,))
            courses = cursor.fetchall()
            return jsonify({'All Lecturer courses': courses}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500



@app.route('/courses/register', methods=['POST'])
def register_student_to_course():
    data = request.get_json()
    studentID = data.get('studentID')
    courseID = data.get('courseID')

    if not all([studentID, courseID]):
        return jsonify({'error': 'Missing studentID or courseID'}), 400

    try:
        
        cursor.execute("SELECT * FROM Student WHERE studentID = %s", (studentID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Student not found'}), 404

        cursor.execute("SELECT * FROM `Course` WHERE courseID = %s", (courseID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Course not found'}), 404

        cursor.execute("SELECT * FROM Enrol WHERE studentID = %s AND courseID = %s", (studentID, courseID))
        if cursor.fetchone():
            return jsonify({'error': 'Student is already registered for this course'}), 409

        cursor.execute("INSERT INTO Enrol (studentID, courseID) VALUES (%s, %s)", (studentID, courseID))
        db.commit()

        return jsonify({'message': 'Student registered for the course successfully'}), 201

    except Error as e:
        return jsonify({'error': str(e)}), 500

   
@app.route('/courses/members', methods=['POST'])
def get_course_members():
    data = request.get_json()
    courseID = data.get('courseID')

    if not courseID:
        return jsonify({'error': 'Missing courseID'}), 400

    try:

        cursor.execute("SELECT * FROM `Course` WHERE courseID = %s", (courseID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Course not found'}), 404

        cursor.execute("""
            SELECT 
                s.studentID,
                a.firstName,
                a.lastName,
                a.acc_contact_info,
                s.department,
                s.gpa
            FROM Enrol e
            JOIN Student s ON e.studentID = s.studentID
            JOIN Account a ON s.accountID = a.accountID
            WHERE e.courseID = %s
        """, (courseID,))

        members = cursor.fetchall()

        return jsonify({'members': members}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/courses/calendar-events/retrieve', methods=['POST'])
def retrieve_calendar_events():
    data = request.get_json()
    courseID = data.get('courseID')
    studentID = data.get('studentID')
    event_date = data.get('event_date')  # format: YYYY-MM-DD

    try:
        # Case 1: Events for a course
        if courseID and not studentID:
            cursor.execute("""
                SELECT * FROM CalendarEvent WHERE courseID = %s
            """, (courseID,))
            events = cursor.fetchall()
            return jsonify({'calendar Events': events}), 200

        # Case 2: Events for a student on a date (via enrolled courses)
        if studentID and event_date:
            cursor.execute("""
                SELECT ce.*
                FROM CalendarEvent ce
                JOIN Enrol e ON ce.courseID = e.courseID
                WHERE e.studentID = %s AND ce.event_date = %s
            """, (studentID, event_date))
            events = cursor.fetchall()
            return jsonify({'calendarEvents': events}), 200
        return jsonify({'error': 'Invalid or missing parameters'}), 400

    except Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/courses/calendar-events/create', methods=['POST'])
def create_calendar_event():
    data = request.get_json()
    courseID = data.get('courseID')
    title = data.get('title')
    description = data.get('description')
    event_date = data.get('event_date')  # expected format: YYYY-MM-DD

    if not all([courseID, title, event_date]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:

        cursor.execute("SELECT * FROM `Course` WHERE courseID = %s", (courseID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Course not found'}), 404

        cursor.execute("""
            INSERT INTO CalendarEvent (courseID, title, description, event_date)
            VALUES (%s, %s, %s, %s)
        """, (courseID, title, description, event_date))

        db.commit()
        return jsonify({'message': 'Calendar event created successfully'}), 201

    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)