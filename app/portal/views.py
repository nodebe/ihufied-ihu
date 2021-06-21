from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required,current_user
from ihufied import db
from . import portal
from app.utils import save_picture, update_picture, insert_picture
from passlib.hash import sha256_crypt as sha256
from app.models import User, Faculty, Department, Course
from app.portal.forms import MakeFacultyForm, MakeDepartmentForm, MakeCourseForm, MakeStudentForm, RegisterStudentCourse,EditStudentCourses

###################
#### ALL-VIEWS ####
###################

@portal.route('/register_student', methods=['GET','POST'])
@login_required
def register_student():
	form = MakeStudentForm()
	if form.validate_on_submit() and form.image.data:
		hashed_password = sha256.encrypt(str(form.firstname.data))		
		try:
			picture_name = save_picture(form.image.data)
			print('saved picture')
			student = User(firstname=form.firstname.data,lastname=form.lastname.data,middlename=form.middlename.data,department_id=str(form.department.data),regnumber=form.regnumber.data,email=form.email.data,phone=form.phone.data,level=form.level.data,password=hashed_password,image_name=picture_name[0],image=picture_name[1])
			print('saved')
			db.session.add(student)
			db.session.commit()
			flash('Student registered successfully.', 'success')
			return redirect(url_for('portal.register_student_courses'))
		except Exception as e:
			#delete_picture(form.image.data)
			flash(str(e), 'warning')
		return redirect(url_for('portal.register_student'))
	return render_template('/portal/register_student.html', form=form)

@portal.route('/register_student_courses', methods=['GET','POST'])
@login_required
def register_student_courses():
	form = RegisterStudentCourse()
	if form.validate_on_submit():
		try:
			student = User.query.filter_by(regnumber=form.regnumber.data).first()
			if student:
				courses = student.department.course_ids
				return render_template('/portal/register_student_courses.html', form=form, courses=courses,student_number=student)
			else:
				flash('Reg number does not exist!', 'warning')
				return redirect(url_for('portal.register_student_courses'))
		except Exception as e:
			flash(str(e), 'warning')
			return redirect(url_for('portal.register_student_courses'))
	return render_template('/portal/register_student_courses.html', form=form, courses=[], student_number='')

@portal.route('/remote_monitoring')
@login_required
def remote_monitoring():
    return render_template('/portal/monitoring.html')

@portal.route('/registered_students', methods= ['GET','POST'])
@login_required
def registered_students():
	page = request.args.get('page', 1 , type=int)
	student= User.query.order_by(User.lastname.asc()).paginate(page=page, per_page=25)
	pupils = User.query.order_by(User.lastname.asc())
	for i in pupils:
		insert_picture(i.image,i.image_name)
	if request.method == 'POST':
		if request.form['detail']:
			the_student= request.form['detail']
			student= User.query.filter_by(id=the_student)	
			return render_template ('/portal/student_details.html',student=student)
	
	else:
		return render_template('/portal/registered_students.html',student =student)

@portal.route('/edit_courses/<student_reg>', methods =['POST','GET'])
@login_required
def edit_courses(student_reg):
	student= User.query.filter_by(regnumber=student_reg).first()
	current=url_for('static', filename='images/' + student.image_name)
	courses=student.department.course_ids #this line gets all the courses for department of this particular student
	form=EditStudentCourses()
	return render_template ('/portal/edit_courses.html',student=student,form=form,current=current,courses=courses)	

@portal.route('/modify_dept')
@login_required  
def modify_dept():
	makefacultyform = MakeFacultyForm()
	makedepartmentform = MakeDepartmentForm()
	makecourseform = MakeCourseForm()
	return render_template('/portal/modify_dept.html',makefacultyform=makefacultyform,makedepartmentform=makedepartmentform,makecourseform=makecourseform)

@portal.route('/create_faculty', methods=['POST'])
@login_required
def create_faculty():
	form = MakeFacultyForm()
	try:
		if form.validate_on_submit():
			faculty = Faculty(name=form.name.data)
			db.session.add(faculty)
			db.session.commit()
			flash('Faculty created!', 'success')
			return redirect(url_for('portal.modify_dept'))
		else:
			flash('Please fill in the form correctly!', 'warning')
			return redirect(url_for('portal.modify_dept'))
	except Exception as e:
		flash('{}'.format(e), 'warning')
		return redirect(url_for('portal.modify_dept'))

@portal.route('/create_department', methods=['POST'])
@login_required
def create_department():
	form = MakeDepartmentForm()
	try:
		if form.validate_on_submit():
			department = Department(name=form.name.data,faculty_id=str(form.faculty.data))
			db.session.add(department)
			db.session.commit()
			flash('Department created!', 'success')
			return redirect(url_for('portal.modify_dept'))
		else:
			flash('Please fill in the form correctly!', 'warning')
			return redirect(url_for('portal.modify_dept'))
	except Exception as e:
		flash('{}'.format(e), 'warning')
		return redirect(url_for('portal.modify_dept'))

@portal.route('/create_course', methods=['POST'])
@login_required
def create_course():
	form = MakeCourseForm()
	try:
		if form.validate_on_submit():
			course = Course(name=form.name.data,department_id=str(form.department.data),title=form.title.data)
			db.session.add(course)
			db.session.commit()
			flash('Course created successfully.', 'success')
			return redirect(url_for('portal.modify_dept'))
		else:
			flash('Please fill in the form correctly!', 'warning')
			return redirect(url_for('portal.modify_dept'))
	except Exception as e:
		flash('{}'.format(e), 'warning')
		return redirect(url_for('portal.modify_dept'))

@portal.route('/submit_registered_courses/<string:student_number>', methods=['POST'])
@login_required
def submit_registered_courses(student_number):
	try:
		student = User.query.filter_by(regnumber=student_number).first()
		form=EditStudentCourses()
		if form.picture.data:
			new_photo=update_picture(form.picture.data)
			student.image_name=new_photo
		print('1: {}'.format(student.course_subscription))
		del student.course_subscription
		print('2: {}'.format(student.course_subscription))
		for title in request.form.getlist('course_select'):
			get_course = Course.query.filter_by(title=title).first()
			get_course.course_subscribers.append(student)
		print('3: {}'.format(student.course_subscription))
		db.session.commit()
		flash('Courses registered successfully!', 'success')
		return redirect(url_for('portal.registered_students'))
	except Exception as e:
		flash(str(e), 'warning')
		return redirect(url_for('portal.register_student_courses'))

@portal.route('/delete_student_data/<string:student_number>')
@login_required
def delete_student_data(student_number):
	try:
		student = User.query.filter_by(regnumber=student_number).first()
		db.session.delete(student)
		db.session.commit()
		flash('Student data removed successfully.', 'success')
		return redirect(url_for('portal.registered_students'))
	except Exception as e:
		flash(str(e), 'warning')
		return redirect(url_for('portal.registered_students'))