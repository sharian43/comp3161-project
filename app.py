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

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

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

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

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

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

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

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

if __name__ == '__main__':
    app.run(debug=True)