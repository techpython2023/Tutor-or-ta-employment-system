from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
from wtforms.validators  import InputRequired, Length, ValidationError

# app = Flask(__name__)

# db= SQLAlchemy()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SECRET_KEY'] ='thisisasecretkey'




db = SQLAlchemy() # db intitialized here
app = Flask(__name__)
app.secret_key = "super secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ="login" 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__='User'
    id= db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    userrole = db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return '<User %r' %self.id
    
   

class Faculty(db.Model):
    __tablename__ ='Faculty'

    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(200),nullable=False)
    campus =db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return 'Faculty %r' %self.id
    


class Department(db.Model):
    __tablename__ ='departments'

    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(200),nullable=False)
    faculty_name =db.Column(db.String(200),nullable=False)
    faculty_id = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return 'Department %r' %self.id


    


@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html')


@app.route('/addadmin')
def addadmin():
    user = User.query.filter_by(email = 'admin2@gmail.com').first()
    if user:
        return redirect(url_for('index'))

    else:
        new_user = User(email ='admin2@gmail.com',password='Admin@123',userrole ='admin')
    try:
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    
    except:
        return 'The was an issue when creating your account'





@app.route('/login',methods= ['POST', 'GET'])
def login():


    if request.method =='POST':
        user_email = request.form['email'].lower()
        user_password = request.form['password']
        user = User.query.filter_by(email = user_email).first()
        
        if user:
            if user.password == user_password:

                login_user(user)
                    
                if user.userrole == 'admin':
                    return redirect(url_for('admin'))

                else:

                     return redirect(url_for('index'))
        
    else:
        return render_template('account/login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')

@app.route('/register',methods=['POST','GET'])
def register():

    if request.method =='POST':
        user_email = request.form['email'].lower()
        user_password = request.form['password']

        new_user = User(email =user_email,password= user_password,userrole ='student')

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        
        except:
            return 'The was an issue when creating your account'



    else:
        users =User.query.all()
        return render_template('account/register.html',users=users)


    


@app.route('/forget_password')
def forget_password():
    return render_template('account/forget_password.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin/admin.html')










@app.route('/faculties',methods=['POST','GET'])
def faculties():

    if request.method =='POST':
        name = request.form['name']
        campus = request.form['campus']

        new_faculty = Faculty(name =name,campus= campus)

        try:
            db.session.add(new_faculty)
            db.session.commit()

            faculties =Faculty.query.all()
            return render_template('admin/faculties.html',faculties=faculties)
        
        except:
            return 'The was an issue adding faculty'



    else:
        faculties =Faculty.query.all()
        return render_template('admin/faculties.html',faculties=faculties)





@app.route('/departments',methods=['POST','GET'])
def departments():

    if request.method =='POST':
        name = request.form['name']
        faculty_name = request.form['faculty_name']
        faculty_id = 1

        new_department = Department(name =name,faculty_name = faculty_name, faculty_id = faculty_id)

        try:
            db.session.add(new_department)
            db.session.commit()

            departments = Department.query.all()
            faculties = Faculty.query.all()

            return render_template('admin/departments.html',departments=departments,faculties= faculties)
        
        except:
            return 'The was an issue adding department'



    else:
        departments =Department.query.all()
        faculties = Faculty.query.all()
        return render_template('admin/departments.html',departments=departments,faculties= faculties)









if __name__ == "__main__":
    app.run(debug = True) 