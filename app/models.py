from . import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

coursesubs = db.Table('coursesubs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    )

class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True )
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128), unique=True)
    confirmed = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')


    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'reset':self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        admin = Admin.query.get(data.get('reset'))
        if admin is None:
            return False
        admin.password = new_password
        db.session.add(admin)
        return True

    
    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    
    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try: 
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')

        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Admin %r>' %self.username
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), default='')
    lastname = db.Column(db.String(30), default='')
    middlename = db.Column(db.String(30), default='')
    regnumber = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), default='')
    phone = db.Column(db.String(15), default='')
    image = db.Column(db.Text)
    image_name = db.Column(db.String(50), default='')
    level = db.Column(db.String(3), default='')
    department_id = db.Column(db.Integer, db.ForeignKey('department.id')) 
    password = db.Column(db.String(120), nullable=False)
    user_status = db.Column(db.String(10), nullable=False, default='student')
    course_subscription = db.relationship('Course', secondary=coursesubs, backref=db.backref('course_subscribers', lazy='dynamic'))
 
    
class Department(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    students = db.relationship('User', backref='department')
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    course_ids = db.relationship('Course', backref='department_course')

    def __repr__(self):
        return '{}'.format(self.id)

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    department_id = db.relationship('Department', backref='faculty_department')

    def __repr__(self):
        return '{}'.format(self.id)

class Course(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    title = db.Column(db.String(10))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    