from flask import Flask, jsonify, request, redirect, url_for, session
import mysql.connector
import json
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your-secret-key'  

db = mysql.connector.connect(host='localhost', user='root', password='', database='')
cursor = db.cursor(dictionary=True)


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    user_id = data.get('user_id')
    h_password = data.get('h_password')
    role = data.get('role')

    if not all([user_id, h_password, role]):
        return jsonify({'error': 'Missing required fields'}), 400

    if role not in ['admin', 'lecturer', 'student']:
        return jsonify({'error': 'Invalid role'}), 400

    hashed_password = generate_password_hash(h_password)

    try:

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if cursor.fetchone():
            return jsonify({'error': 'User already exists'}), 409

        cursor.execute(
            "INSERT INTO users (user_id, h_password, role) VALUES (%s, %s, %s)",
            (user_id, hashed_password, role)
        )

        if role == 'student':
            #StudentID = data.get('StudentID')
            FirstName = data.get('FirstName')
            LastName = data.get('LastName')
            if not all([user_id, FirstName, LastName]):
                return jsonify({'error': 'Missing student details'}), 400
            cursor.execute(
                "INSERT INTO students (StudentID, FirstName, LastName) VALUES (%s, %s, %s)",
                (user_id, FirstName, LastName)
            )

        elif role == 'lecturer':
            #LecID = data.get('LecID')
            LecName = data.get('LecName')
            Department = data.get('Department')
            if not all([user_id, LecName, Department]):
                return jsonify({'error': 'Missing lecturer details'}), 400
            cursor.execute(
                "INSERT INTO lecturers (LecID, LecName, Department) VALUES (%s, %s, %s)",
                (user_id, LecName, Department)
            )

        elif role == 'admin':
            cursor.execute(
                "INSERT INTO admins (user_id, h_password) VALUES (%s, %s)",
                (user_id, hashed_password)
            )

        db.commit()
        return jsonify({'message': f'{role.capitalize()} registered successfully'}), 201

    except Error as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


@app.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()
    user_id = data.get('user_id')
    h_password = data.get('h_password')

    if not all([user_id, h_password]):
        return jsonify({'error': 'Missing login credentials'}), 400

    try:

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user['h_password'], h_password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        session['user_id'] = user['user_id']
        session['role'] = user['role']
        return jsonify({'message': 'Login successful'}), 200

    except Error as e:
        #redirect(url_for('home'))
        #return jsonify({'redirect': '/home'})
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
            
            
def is_admin():
    return session.get('user_id') and session.get('role') == 'admin'

@app.route('/create-course', methods=['POST'])
def create_course():
    if not is_admin():
        return jsonify({'error': 'Unauthorized. Admins only.'}), 403
    
    data = request.get_json()
    course_id = data.get('CourseID')
    course_name = data.get('CourseName')
    lec_id = data.get('LecID')

    if not all([course_id, course_name, lec_id]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:

        cursor.execute("SELECT role FROM users WHERE user_id = %s", (lec_id,))
        lecturer = cursor.fetchone()
        if not lecturer or lecturer[0] != 'lecturer':
            return jsonify({'error': 'Lecturer not identified'}), 400

        cursor.execute("SELECT * FROM courses WHERE CourseID = %s", (course_id,))
        if cursor.fetchone():
            return jsonify({'error': 'Course already exists'}), 409

        cursor.execute(
            "INSERT INTO courses (CourseID, CourseName, LecID) VALUES (%s, %s, %s)",
            (course_id, course_name, lec_id)
        )
        db.commit()

        return jsonify({'message': 'Course created successfully'}), 201

    except Error as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


@app.route('/retrieve-courses', methods=['POST'])
def retrieve_courses():
    data = request.get_json()

    student_id = data.get('student_id')
    lecturer_id = data.get('lecturer_id')

    try:

        # Case 1: Get all courses
        if not student_id and not lecturer_id:
            cursor.execute("SELECT CourseID, CourseName, LecID FROM courses")
            courses = cursor.fetchall()
            return jsonify({'all_courses': courses}), 200

        # Case 2: Get courses for a particular student
        if student_id:
            cursor.execute("""
                SELECT c.CourseID, c.CourseName, c.LecID
                FROM courses c
                JOIN registrations r ON c.CourseID = r.CourseID
                WHERE r.StudentID = %s
            """, (student_id,))
            courses = cursor.fetchall()
            return jsonify({'courses_for_student': courses}), 200

        # Case 3: Get courses taught by a particular lecturer
        if lecturer_id:
            cursor.execute("""
                SELECT CourseID, CourseName
                FROM courses
                WHERE LecID = %s
            """, (lecturer_id,))
            courses = cursor.fetchall()
            return jsonify({'courses_by_lecturer': courses}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()



if __name__ == '__main__':
    app.run(debug=True)