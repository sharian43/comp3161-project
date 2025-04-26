from flask import Flask, jsonify, request, redirect, url_for, session, flash, render_template
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import forms

load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

db=mysql.connector.connect(user='dbms', password='finalproject', host='127.0.0.1',database='cms')
#db = mysql.connector.connect(host='localhost', user=os.getenv('DB_User'), password= os.getenv('DB_Password'), database='cms')
cursor = db.cursor(dictionary=True)


@app.route('/register/user', methods=['POST'])
def register_user():
    data = request.form
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

    data = request.form
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

    data = request.form
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

    data = request.form
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



@app.route('/login', methods=['GET','POST'])
def user_login():
    #A login class to represent and validate our client-side form data.
    form = forms.LoginForm()
    print('lol')

    #Login and validate the user.
    if form.validate_on_submit():
        username = form.username.data
        userPassword = form.password.data



     #if not all([username, userPassword]):
     #   return jsonify({'error': 'Missing login credentials'}), 400

        try:

            cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
            user = cursor.fetchone()

            if not user or not check_password_hash(user['userPassword'], userPassword):
                flash('Invalid credentials')
                return jsonify({'error': 'Invalid credentials'}), 401
            else:
                userID = user['userID']

                cursor.execute("SELECT * FROM Account WHERE userID = %s", (userID,))
                account = cursor.fetchone()

                accRole = account['accRole']

                if accRole not in ['STUDENT', 'LECTURER', 'ADMIN']:
                    flash('User MUST BE any of the following, an admin, a student or a lecturer')
                    return jsonify({'error': 'Cannot login'}), 403
                else:

                    cursor.execute("INSERT INTO Login (userID) VALUES (%s)", (userID,))
                    db.commit()
                    
                    session['userID'] = user['userID']
                    session['accRole'] = account['accRole']
                    
                    print("Successful")
                    return jsonify({'message': 'Login successful', 'Role': accRole}), 200, redirect(url_for('dashboard'))     
        except Error as e:
            return jsonify({'error': str(e)}), 500
        
    return render_template('Login.html', form=form)  



@app.route('/courses/create-course', methods=['POST'])
def create_course():
    data = request.form
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


@app.route('/courses/retrieve-courses', methods=['GET'])
def retrieve_courses():
    data = request.form

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
    data = request.form
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
    data = request.form
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
    data = request.form
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
    data = request.form
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

@app.route('/forums/retrieve', methods=['POST'])
def retrieve_forums():
    data = request.form
    courseID = data.get('courseID')

    if not courseID:
        return jsonify({'error': 'Missing courseID'}), 400

    try:
        # Verify the course exists
        cursor.execute("SELECT * FROM Course WHERE courseID = %s", (courseID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Course not found'}), 404

        # Retrieve all forums for the specified course
        cursor.execute("""
            SELECT f.forumID, f.topic, f.creator, u.username as creator_name
            FROM DiscussionForum f
            JOIN User u ON f.creator = u.userID
            WHERE f.courseID = %s
        """, (courseID,))
        
        forums = cursor.fetchall()
        return jsonify({'forums': forums}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/forums/create', methods=['POST'])
def create_forum():
    data = request.form
    courseID = data.get('courseID')
    topic = data.get('topic')

    if not all([courseID, topic]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        if 'userID' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        
        userID = session['userID']

        cursor.execute("SELECT * FROM Course WHERE courseID = %s", (courseID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Course not found'}), 404

        cursor.execute("SELECT * FROM DiscussionForum WHERE courseID = %s", (courseID,))
        if cursor.fetchone():
            return jsonify({'error': 'A forum already exists for this course'}), 409

        cursor.execute("""
            INSERT INTO DiscussionForum (courseID, topic, creator)
            VALUES (%s, %s, %s)
        """, (courseID, topic, userID))
        
        db.commit()
        return jsonify({'message': 'Forum created successfully'}), 201

    except Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/threads/retrieve', methods=['POST'])
def retrieve_threads():
    data = request.form
    forumID = data.get('forumID')

    if not forumID:
        return jsonify({'error': 'Missing forumID'}), 400

    try:
        cursor.execute("SELECT * FROM DiscussionForum WHERE forumID = %s", (forumID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Forum not found'}), 404

        # Retrieve all threads for the specified forum
        cursor.execute("""
            SELECT 
                t.threadID, 
                t.title, 
                t.content, 
                t.time, 
                t.parentThreadID,
                u.username as author
            FROM DiscussionThread t
            JOIN User u ON t.userID = u.userID
            WHERE t.forumID = %s
            ORDER BY 
                CASE WHEN t.parentThreadID IS NULL THEN t.threadID ELSE t.parentThreadID END,
                t.threadID
        """, (forumID,))
        
        threads = cursor.fetchall()
        
        # Organize threads 
        thread_dict = {}
        root_threads = []
        
        for thread in threads:
            thread_id = thread['threadID']
            thread_dict[thread_id] = {
                'threadID': thread['threadID'],
                'title': thread['title'],
                'content': thread['content'],
                'time': thread['time'].isoformat() if thread['time'] else None,
                'author': thread['author'],
                'replies': []
            }
        
        for thread in threads:
            thread_id = thread['threadID']
            parent_id = thread['parentThreadID']
            
            if parent_id is None:
                root_threads.append(thread_dict[thread_id])
            else:
                # This is a reply
                if parent_id in thread_dict:
                    thread_dict[parent_id]['replies'].append(thread_dict[thread_id])
        
        return jsonify({'threads': root_threads}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/threads/create', methods=['POST'])
def create_thread():
    data = request.form
    forumID = data.get('forumID')
    title = data.get('title')
    content = data.get('content')

    if not all([forumID, title, content]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        if 'userID' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        
        userID = session['userID']

        cursor.execute("SELECT * FROM DiscussionForum WHERE forumID = %s", (forumID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Forum not found'}), 404

        # Create the thread
        cursor.execute("""
            INSERT INTO DiscussionThread (forumID, userID, title, content, parentThreadID)
            VALUES (%s, %s, %s, %s, NULL)
        """, (forumID, userID, title, content))
        
        db.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        threadID = cursor.fetchone()['LAST_INSERT_ID()']
        
        return jsonify({
            'message': 'Thread created successfully',
            'threadID': threadID
        }), 201

    except Error as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/threads/reply', methods=['POST'])
def reply_to_thread():
    data = request.form
    parentThreadID = data.get('parentThreadID')
    content = data.get('content')

    if not all([parentThreadID, content]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        if 'userID' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        
        userID = session['userID']

        # Verify the parent thread exists
        cursor.execute("SELECT forumID FROM DiscussionThread WHERE threadID = %s", (parentThreadID,))
        parent_thread = cursor.fetchone()
        if not parent_thread:
            return jsonify({'error': 'Parent thread not found'}), 404
        
        forumID = parent_thread['forumID']

        # Create the reply - title is NULL for replies
        cursor.execute("""
            INSERT INTO DiscussionThread (forumID, userID, title, content, parentThreadID)
            VALUES (%s, %s, NULL, %s, %s)
        """, (forumID, userID, content, parentThreadID))
        
        db.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        replyID = cursor.fetchone()['LAST_INSERT_ID()']
        
        return jsonify({
            'message': 'Reply posted successfully',
            'replyID': replyID
        }), 201

    except Error as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    

@app.route('/sections/create', methods=['POST'])
def create_section():
    data = request.form
    courseID = data.get('courseID')
    section_name = data.get('section_name')

    if not all([courseID, section_name]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        if 'userID' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        
        userID = session['userID']
        
        # Check if user is a lecturer for this course
        cursor.execute("""
            SELECT l.lecturerID
            FROM Lecturer l
            JOIN Account a ON l.accountID = a.accountID
            JOIN Course c ON l.lecturerID = c.lecturerID
            WHERE a.userID = %s AND c.courseID = %s
        """, (userID, courseID))
        
        lecturer = cursor.fetchone()
        if not lecturer and session['accRole'] != 'ADMIN':
            return jsonify({'error': 'You are not authorized to add content to this course'}), 403

        # Verify the course exists
        cursor.execute("SELECT * FROM Course WHERE courseID = %s", (courseID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Course not found'}), 404

        # Create the section
        cursor.execute("""
            INSERT INTO Section (courseID, section_name)
            VALUES (%s, %s)
        """, (courseID, section_name))
        
        db.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        sectionID = cursor.fetchone()['LAST_INSERT_ID()']
        
        return jsonify({
            'message': 'Section created successfully',
            'sectionID': sectionID
        }), 201

    except Error as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/sections/items/add-assignment', methods=['POST'])
def add_assignment():
    data = request.form
    sectionID = data.get('sectionID')
    assignmentName = data.get('assignmentName')
    maxPoints = data.get('maxPoints', 100.00)
    weight = data.get('weight', 1.00)
    
    if not all([sectionID, assignmentName]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        if 'userID' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        
        userID = session['userID']
        
        cursor.execute("""
            SELECT l.lecturerID
            FROM Lecturer l
            JOIN Account a ON l.accountID = a.accountID
            JOIN Course c ON l.lecturerID = c.lecturerID
            JOIN Section s ON c.courseID = s.courseID
            WHERE a.userID = %s AND s.sectionID = %s
        """, (userID, sectionID))
        
        lecturer = cursor.fetchone()
        if not lecturer and session['accRole'] != 'ADMIN':
            return jsonify({'error': 'You are not authorized to add content to this section'}), 403

        # Verify the section exists
        cursor.execute("SELECT * FROM Section WHERE sectionID = %s", (sectionID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Section not found'}), 404

        # Create a section item
        cursor.execute("""
            INSERT INTO SectionItem (sectionID, item_type)
            VALUES (%s, 'ASSIGNMENT')
        """, (sectionID,))
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        itemID = cursor.fetchone()['LAST_INSERT_ID()']
        
        # Create the assignment
        cursor.execute("""
            INSERT INTO Assignment (itemID, assignmentName, maxPoints, weight)
            VALUES (%s, %s, %s, %s)
        """, (itemID, assignmentName, maxPoints, weight))
        
        db.commit()
        
        return jsonify({
            'message': 'Assignment added successfully',
            'itemID': itemID
        }), 201

    except Error as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/sections/items/add-slide', methods=['POST'])
def add_lecture_slide():
    data = request.form
    sectionID = data.get('sectionID')
    slide_name = data.get('slide_name')

    if not all([sectionID, slide_name]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        if 'userID' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        
        userID = session['userID']
        
        cursor.execute("""
            SELECT l.lecturerID
            FROM Lecturer l
            JOIN Account a ON l.accountID = a.accountID
            JOIN Course c ON l.lecturerID = c.lecturerID
            JOIN Section s ON c.courseID = s.courseID
            WHERE a.userID = %s AND s.sectionID = %s
        """, (userID, sectionID))
        
        lecturer = cursor.fetchone()
        if not lecturer and session['accRole'] != 'ADMIN':
            return jsonify({'error': 'You are not authorized to add content to this section'}), 403

        # Verify the section exists
        cursor.execute("SELECT * FROM Section WHERE sectionID = %s", (sectionID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Section not found'}), 404

        # Create a section item
        cursor.execute("""
            INSERT INTO SectionItem (sectionID, item_type)
            VALUES (%s, 'LECTURE_SLIDE')
        """, (sectionID,))
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        itemID = cursor.fetchone()['LAST_INSERT_ID()']
        
        # Create the lecture slide
        cursor.execute("""
            INSERT INTO LectureSlide (itemID, slide_name)
            VALUES (%s, %s)
        """, (itemID, slide_name))
        
        db.commit()
        
        return jsonify({
            'message': 'Lecture slide added successfully',
            'itemID': itemID
        }), 201

    except Error as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/sections/items/add-link', methods=['POST'])
def add_link():
    data = request.form
    sectionID = data.get('sectionID')
    link_title = data.get('link_title')
    url = data.get('url')
    description = data.get('description')

    if not all([sectionID, link_title, url]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        if 'userID' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        
        userID = session['userID']
        
        cursor.execute("""
            SELECT l.lecturerID
            FROM Lecturer l
            JOIN Account a ON l.accountID = a.accountID
            JOIN Course c ON l.lecturerID = c.lecturerID
            JOIN Section s ON c.courseID = s.courseID
            WHERE a.userID = %s AND s.sectionID = %s
        """, (userID, sectionID))
        
        lecturer = cursor.fetchone()
        if not lecturer and session['accRole'] != 'ADMIN':
            return jsonify({'error': 'You are not authorized to add content to this section'}), 403

        # Verify the section exists
        cursor.execute("SELECT * FROM Section WHERE sectionID = %s", (sectionID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Section not found'}), 404

        # Create a section item
        cursor.execute("""
            INSERT INTO SectionItem (sectionID, item_type)
            VALUES (%s, 'LINK')
        """, (sectionID,))
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        itemID = cursor.fetchone()['LAST_INSERT_ID()']
        
        # Create the link
        cursor.execute("""
            INSERT INTO Link (itemID, link_title, url, description)
            VALUES (%s, %s, %s, %s)
        """, (itemID, link_title, url, description))
        
        db.commit()
        
        return jsonify({
            'message': 'Link added successfully',
            'itemID': itemID
        }), 201

    except Error as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/sections/items/add-file', methods=['POST'])
def add_file():
    data = request.form
    sectionID = data.get('sectionID')
    file_name = data.get('file_name')
    file_path = data.get('file_path')
    file_type = data.get('file_type')
    file_size = data.get('file_size')

    if not all([sectionID, file_name, file_path]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        if 'userID' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        
        userID = session['userID']
        
        cursor.execute("""
            SELECT l.lecturerID
            FROM Lecturer l
            JOIN Account a ON l.accountID = a.accountID
            JOIN Course c ON l.lecturerID = c.lecturerID
            JOIN Section s ON c.courseID = s.courseID
            WHERE a.userID = %s AND s.sectionID = %s
        """, (userID, sectionID))
        
        lecturer = cursor.fetchone()
        if not lecturer and session['accRole'] != 'ADMIN':
            return jsonify({'error': 'You are not authorized to add content to this section'}), 403

        # Verify the section exists
        cursor.execute("SELECT * FROM Section WHERE sectionID = %s", (sectionID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Section not found'}), 404

        # Create a section item
        cursor.execute("""
            INSERT INTO SectionItem (sectionID, item_type)
            VALUES (%s, 'FILE')
        """, (sectionID,))
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        itemID = cursor.fetchone()['LAST_INSERT_ID()']
        
        # Create the file
        cursor.execute("""
            INSERT INTO File (itemID, file_name, file_path, file_type, file_size)
            VALUES (%s, %s, %s, %s, %s)
        """, (itemID, file_name, file_path, file_type, file_size))
        
        db.commit()
        
        return jsonify({
            'message': 'File added successfully',
            'itemID': itemID
        }), 201

    except Error as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/courses/content/retrieve', methods=['POST'])
def retrieve_course_content():
    data = request.form
    courseID = data.get('courseID')

    if not courseID:
        return jsonify({'error': 'Missing courseID'}), 400

    try:
        # Verify the course exists
        cursor.execute("SELECT * FROM Course WHERE courseID = %s", (courseID,))
        if not cursor.fetchone():
            return jsonify({'error': 'Course not found'}), 404

        studentID = None
        if 'userID' in session and session['accRole'] == 'STUDENT':
            cursor.execute("""
                SELECT s.studentID
                FROM Student s
                JOIN Account a ON s.accountID = a.accountID
                WHERE a.userID = %s
            """, (session['userID'],))
            student = cursor.fetchone()
            if student:
                studentID = student['studentID']

        # Retrieve all sections for the course
        cursor.execute("""
            SELECT sectionID, section_name
            FROM Section
            WHERE courseID = %s
            ORDER BY sectionID
        """, (courseID,))
        
        sections = cursor.fetchall()
        result = []
        
        # For each section, retrieve its content items
        for section in sections:
            sectionID = section['sectionID']
            
            # Get all section items
            cursor.execute("""
                SELECT itemID, item_type
                FROM SectionItem
                WHERE sectionID = %s
            """, (sectionID,))
            
            items = cursor.fetchall()
            section_content = []
            
            # For each item, get the specific content based on its type
            for item in items:
                itemID = item['itemID']
                item_type = item['item_type']
                
                if item_type == 'LECTURE_SLIDE':
                    cursor.execute("""
                        SELECT slideID, slide_name
                        FROM LectureSlide
                        WHERE itemID = %s
                    """, (itemID,))
                    slide = cursor.fetchone()
                    if slide:
                        section_content.append({
                            'type': 'slide',
                            'id': slide['slideID'],
                            'name': slide['slide_name']
                        })
                
                elif item_type == 'LINK':
                    cursor.execute("""
                        SELECT linkID, link_title, url, description
                        FROM Link
                        WHERE itemID = %s
                    """, (itemID,))
                    link = cursor.fetchone()
                    if link:
                        section_content.append({
                            'type': 'link',
                            'id': link['linkID'],
                            'title': link['link_title'],
                            'url': link['url'],
                            'description': link['description']
                        })
                
                elif item_type == 'FILE':
                    cursor.execute("""
                        SELECT fileID, file_name, file_path, file_type, file_size, upload_date
                        FROM File
                        WHERE itemID = %s
                    """, (itemID,))
                    file = cursor.fetchone()
                    if file:
                        section_content.append({
                            'type': 'file',
                            'id': file['fileID'],
                            'name': file['file_name'],
                            'path': file['file_path'],
                            'file_type': file['file_type'],
                            'size': file['file_size'],
                            'upload_date': file['upload_date'].isoformat() if file['upload_date'] else None
                        })
                
                elif item_type == 'ASSIGNMENT':
                    cursor.execute("""
                        SELECT assignmentID, assignmentName, maxPoints, weight
                        FROM Assignment
                        WHERE itemID = %s
                    """, (itemID,))
                    assignment = cursor.fetchone()
                    if assignment:
                        assignment_data = {
                            'type': 'assignment',
                            'id': assignment['assignmentID'],
                            'name': assignment['assignmentName'],
                            'maxPoints': float(assignment['maxPoints']),
                            'weight': float(assignment['weight'])
                        }
                        
                        # If the user is a student, get their submission and grade
                        if studentID:
                            cursor.execute("""
                                SELECT submissionID, submissionContent, submissionDate, grade
                                FROM AssignmentSubmission
                                WHERE assignmentID = %s AND studentID = %s
                            """, (assignment['assignmentID'], studentID))
                            submission = cursor.fetchone()
                            if submission:
                                assignment_data['submitted'] = True
                                assignment_data['submissionID'] = submission['submissionID']
                                assignment_data['submissionDate'] = submission['submissionDate'].isoformat() if submission['submissionDate'] else None
                                assignment_data['grade'] = float(submission['grade']) if submission['grade'] is not None else None
                            else:
                                assignment_data['submitted'] = False
                        
                        # If the user is a lecturer, get submission stats
                        elif session.get('accRole') == 'LECTURER':
                            cursor.execute("""
                                SELECT COUNT(*) AS total_submissions,
                                       SUM(CASE WHEN grade IS NOT NULL THEN 1 ELSE 0 END) AS graded_submissions
                                FROM AssignmentSubmission
                                WHERE assignmentID = %s
                            """, (assignment['assignmentID'],))
                            stats = cursor.fetchone()
                            if stats:
                                assignment_data['total_submissions'] = stats['total_submissions']
                                assignment_data['graded_submissions'] = stats['graded_submissions']
                        
                        section_content.append(assignment_data)
            
            # Add section with its content to the result
            result.append({
                'sectionID': section['sectionID'],
                'section_name': section['section_name'],
                'content': section_content
            })
        
        return jsonify({'course_content': result}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/assignments/submit', methods=['POST'])
def submit_assignment():
    data = request.form
    assignmentID = data.get('assignmentID')
    submissionContent = data.get('submissionContent')
    
    if not all([assignmentID, submissionContent]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        if 'userID' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        
        if session['accRole'] != 'STUDENT':
            return jsonify({'error': 'Only students can submit assignments'}), 403
        
        userID = session['userID']
        
        # Get the student's ID
        cursor.execute("""
            SELECT s.studentID
            FROM Student s
            JOIN Account a ON s.accountID = a.accountID
            WHERE a.userID = %s
        """, (userID,))
        
        student = cursor.fetchone()
        if not student:
            return jsonify({'error': 'Student record not found'}), 404
        
        studentID = student['studentID']
        
        # Check if the assignment exists and get course information
        cursor.execute("""
            SELECT a.assignmentID, s.sectionID, s.courseID
            FROM Assignment a
            JOIN SectionItem si ON a.itemID = si.itemID
            JOIN Section s ON si.sectionID = s.sectionID
            WHERE a.assignmentID = %s
        """, (assignmentID,))
        
        assignment_info = cursor.fetchone()
        if not assignment_info:
            return jsonify({'error': 'Assignment not found'}), 404
        
        courseID = assignment_info['courseID']
        
        # Check if the student is enrolled in the course
        cursor.execute("""
            SELECT * FROM Enrol
            WHERE studentID = %s AND courseID = %s
        """, (studentID, courseID))
        
        if not cursor.fetchone():
            return jsonify({'error': 'You are not enrolled in this course'}), 403
        
        # Check if the student has already submitted this assignment
        cursor.execute("""
            SELECT submissionID FROM AssignmentSubmission
            WHERE studentID = %s AND assignmentID = %s
        """, (studentID, assignmentID))
        
        existing_submission = cursor.fetchone()
        
        if existing_submission:
            # Update existing submission
            cursor.execute("""
                UPDATE AssignmentSubmission
                SET submissionContent = %s, submissionDate = CURRENT_TIMESTAMP
                WHERE submissionID = %s
            """, (submissionContent, existing_submission['submissionID']))
            
            db.commit()
            return jsonify({
                'message': 'Assignment resubmitted successfully',
                'submissionID': existing_submission['submissionID']
            }), 200
        else:
            # Create new submission
            cursor.execute("""
                INSERT INTO AssignmentSubmission (assignmentID, studentID, submissionContent)
                VALUES (%s, %s, %s)
            """, (assignmentID, studentID, submissionContent))
            
            db.commit()
            
            cursor.execute("SELECT LAST_INSERT_ID()")
            submissionID = cursor.fetchone()['LAST_INSERT_ID()']
            
            return jsonify({
                'message': 'Assignment submitted successfully',
                'submissionID': submissionID
            }), 201
            
    except Error as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    


@app.route('/assignments/grade', methods=['POST'])
def grade_assignment():
    data = request.form
    submissionID = data.get('submissionID')
    grade = data.get('grade')
    
    if not all([submissionID, grade is not None]):  # Allow grade of 0
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        if 'userID' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        
        if session['accRole'] not in ['LECTURER', 'ADMIN']:
            return jsonify({'error': 'Only lecturers and admins can grade assignments'}), 403
        
        userID = session['userID']
        
        cursor.execute("START TRANSACTION")
        
        # Get submission details including student and assignment info
        cursor.execute("""
            SELECT 
                sub.studentID,
                a.assignmentID,
                a.maxPoints,
                s.courseID
            FROM AssignmentSubmission sub
            JOIN Assignment a ON sub.assignmentID = a.assignmentID
            JOIN SectionItem si ON a.itemID = si.itemID
            JOIN Section s ON si.sectionID = s.sectionID
            WHERE sub.submissionID = %s
        """, (submissionID,))
        
        submission_info = cursor.fetchone()
        if not submission_info:
            db.rollback()
            return jsonify({'error': 'Submission not found'}), 404
        
        studentID = submission_info['studentID']
        courseID = submission_info['courseID']
        maxPoints = submission_info['maxPoints']
        
        # If lecturer, check if they teach this course
        if session['accRole'] == 'LECTURER':
            cursor.execute("""
                SELECT l.lecturerID
                FROM Lecturer l
                JOIN Account a ON l.accountID = a.accountID
                JOIN Course c ON l.lecturerID = c.lecturerID
                WHERE a.userID = %s AND c.courseID = %s
            """, (userID, courseID))
            
            if not cursor.fetchone():
                db.rollback()
                return jsonify({'error': 'You are not authorized to grade assignments for this course'}), 403
        
        # Validate grade is within allowed range
        if float(grade) < 0 or float(grade) > float(maxPoints):
            db.rollback()
            return jsonify({'error': f'Grade must be between 0 and {maxPoints}'}), 400
        
        # Update the grade
        cursor.execute("""
            UPDATE AssignmentSubmission 
            SET grade = %s
            WHERE submissionID = %s
        """, (grade, submissionID))
        
        # Calculate the student's overall GPA from all graded assignments
        cursor.execute("""
            SELECT AVG(
                (sub.grade / a.maxPoints) * 4.0  -- Convert to 4.0 scale
            ) AS newGPA
            FROM AssignmentSubmission sub
            JOIN Assignment a ON sub.assignmentID = a.assignmentID
            WHERE sub.studentID = %s
            AND sub.grade IS NOT NULL
        """, (studentID,))
        
        gpa_result = cursor.fetchone()
        new_gpa = gpa_result['newGPA'] if gpa_result and gpa_result['newGPA'] is not None else 0.00
        
        # Cap GPA at 4.0 if needed
        if float(new_gpa) > 4.0:
            new_gpa = 4.0
        
        # Update student GPA
        cursor.execute("""
            UPDATE Student 
            SET gpa = %s
            WHERE studentID = %s
        """, (new_gpa, studentID))
        
        db.commit()
        
        # Get student name for the response
        cursor.execute("""
            SELECT firstName, lastName
            FROM Student
            WHERE studentID = %s
        """, (studentID,))
        
        student = cursor.fetchone()
        student_name = f"{student['firstName']} {student['lastName']}" if student else "Unknown Student"
        
        return jsonify({
            'message': f'Assignment graded successfully for {student_name}',
            'grade': float(grade),
            'maxPoints': float(maxPoints),
            'percentage': (float(grade) / float(maxPoints)) * 100,
            'newGPA': float(new_gpa)
        }), 200
        
    except Error as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500



#Get all courses that have 50 or more students
@app.route('/reports/courses-with-many-students', methods=['GET'])
def courses_with_many_students():
    try:
        cursor.execute("""
            SELECT c.courseID, c.course_name, c.course_code, COUNT(e.studentID) AS student_count
            FROM Course c
            JOIN Enrol e ON c.courseID = e.courseID
            GROUP BY c.courseID, c.course_name, c.course_code
            HAVING COUNT(e.studentID) >= 50
        """)
        
        courses = cursor.fetchall()
        return jsonify({'courses_with_50_plus_students': courses}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500

# Get all students that do 5 or more courses
@app.route('/reports/students-with-many-courses', methods=['GET'])
def students_with_many_courses():
    try:
        cursor.execute("""
            SELECT s.studentID, a.firstName, a.lastName, COUNT(e.courseID) AS course_count
            FROM Student s
            JOIN Account a ON s.accountID = a.accountID
            JOIN Enrol e ON s.studentID = e.studentID
            GROUP BY s.studentID, a.firstName, a.lastName
            HAVING COUNT(e.courseID) >= 5
        """)
        
        students = cursor.fetchall()
        return jsonify({'students_with_5_plus_courses': students}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500

#Get all lecturers that teach 3 or more courses
@app.route('/reports/lecturers-with-many-courses', methods=['GET'])
def lecturers_with_many_courses():
    try:
        cursor.execute("""
            SELECT l.lecturerID, a.firstName, a.lastName, COUNT(c.courseID) AS course_count
            FROM Lecturer l
            JOIN Account a ON l.accountID = a.accountID
            JOIN Course c ON l.lecturerID = c.lecturerID
            GROUP BY l.lecturerID, a.firstName, a.lastName
            HAVING COUNT(c.courseID) >= 3
        """)
        
        lecturers = cursor.fetchall()
        return jsonify({'lecturers_with_3_plus_courses': lecturers}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500

#Get the 10 most enrolled courses
@app.route('/reports/top-enrolled-courses', methods=['GET'])
def top_enrolled_courses():
    try:
        cursor.execute("""
            SELECT c.courseID, c.course_name, c.course_code, COUNT(e.studentID) AS enrollment_count
            FROM Course c
            JOIN Enrol e ON c.courseID = e.courseID
            GROUP BY c.courseID, c.course_name, c.course_code
            ORDER BY COUNT(e.studentID) DESC
            LIMIT 10
        """)
        
        courses = cursor.fetchall()
        return jsonify({'top_10_enrolled_courses': courses}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500

#Get the top 10 students with the highest overall averages (GPA)
@app.route('/reports/top-students', methods=['GET'])
def top_students_by_gpa():
    try:
        cursor.execute("""
            SELECT s.studentID, a.firstName, a.lastName, s.department, s.gpa
            FROM Student s
            JOIN Account a ON s.accountID = a.accountID
            ORDER BY s.gpa DESC
            LIMIT 10
        """)
        
        students = cursor.fetchall()
        return jsonify({'top_10_students_by_gpa': students}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)