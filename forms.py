from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

#WTform for Login Page
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])

#WTform for Register User Page
class CreateAccount(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    acc_contact_info = StringField('Contact', validators=[InputRequired()])
    department = StringField('Department', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    accPassword = StringField('Password', validators=[InputRequired()])

#WTForm for creating a course
class CreateCourse(FlaskForm):
    course_name = StringField('Course Name', validators=[InputRequired()])
    course_code = StringField('Course Code',  validators=[InputRequired()])
    lecturerID = StringField('Lecturer ID',  validators=[InputRequired()])
   