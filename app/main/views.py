from datetime import datetime
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app.models import Course
import json
import base64
from . import main


###################
#### ALL-VIEWS ####
###################
@main.route('/')
def index():
    return render_template('index.html',current_time=datetime.utcnow())

@main.route('/getuser/<string:course_title>')
def getuser(course_title):
    try:
        course_title= course_title.upper()
        course = Course.query.filter_by(title=course_title).first()
        users = course.course_subscribers
        students_list = []
        for student in users:
            students = {}
            students['firstname'] = student.firstname
            students['lastname'] = student.lastname
            students['reg_no'] = student.regnumber
            #convert the students image stored in bytes to str so it can be passable with json on line 41
            students['img'] = student.image 
            students_list.append(students)
        if students_list == []:
            return 'No student registered!'
        else:
            print(students_list)
            return json.dumps(students_list)
    except Exception as e:
        return str(e)

#getting only students in that department registered can be done by inserting the id into the routing channel

global student_reg_nos

student_reg_nos = []

@main.route('/poststudent', methods = ['POST'])
def poststudent():
    student_and_course = {}
    data = json.loads(request.get_data())
    student_and_course['reg_no'] = data['reg_no']
    student_and_course['course_code'] = data['coursecode']
    student_reg_nos.append(student_and_course)

@main.route('/clearstudents')
def clearstudents():
    student_reg_nos = []
    return redirect(url_for('portal.remote_monitoring'))