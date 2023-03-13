from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
from wtforms.validators  import InputRequired, Length, ValidationError
import getpass
import urllib.parse
import requests
from flask import Flask
from flask_mail import Mail, Message

from urllib import parse


# app = Flask(__name__)

# db= SQLAlchemy()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SECRET_KEY'] ='thisisasecretkey'




db = SQLAlchemy() # db intitialized here
app = Flask(__name__)
app.secret_key = "super secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)



# mail= Mail(app)

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
# app.config['MAIL_PASSWORD'] = '*****'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)



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
    

class Course(db.Model):
    __tablename__ ='courses'

    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(200),nullable=False)
    department_name =db.Column(db.String(200),nullable=False)
    department_id = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return 'Course %r' %self.id
    

class Module(db.Model):
    __tablename__ ='modules'

    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(200),nullable=False)
    course_name =db.Column(db.String(200),nullable=False)
    course_id = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return 'Module %r' %self.id
    

class Departmenthod(db.Model):
    __tablename__ ='departmenthods'

    id = db.Column(db.Integer,primary_key =True)
    department_name = db.Column(db.String(200),nullable=False)
    department_id =db.Column(db.Integer,nullable=False)
    hod_email =db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return 'Departmenthod %r' %self.id


class Modulelecture(db.Model):
    __tablename__ ='modulelectures'

    id = db.Column(db.Integer,primary_key =True)
    Lecture_email = db.Column(db.String(200),nullable=False)
    module_name =db.Column(db.String(200),nullable=False)
    module_id =db.Column(db.Integer,nullable=False)
    lecture_id =db.Column(db.Integer,nullable=False)
    

    def __repr__(self):
        return 'Modulelecture %r' %self.id
    


class Tarequest(db.Model):
    __tablename__ ='tarequests'

    id = db.Column(db.Integer,primary_key =True)
    Lecture_email = db.Column(db.String(200),nullable=False)
    lecture_id =db.Column(db.Integer,nullable=False)
    modulelecture_id =db.Column(db.Integer,nullable=False)
    module_name =db.Column(db.String(200),nullable=False)
    module_id =db.Column(db.Integer,nullable=False)
    hod_email =db.Column(db.String(200),nullable=False)
    hod_id =db.Column(db.Integer,nullable=False)
    request_status =db.Column(db.String(200),nullable=False)
    request_statusnum =db.Column(db.Integer,nullable=False)
    request_reason =db.Column(db.String(200),nullable=False)



    def __repr__(self):
        return 'Tarequest %r' %self.id
    




class Taopening(db.Model):
    __tablename__ ='taopenings'

    id = db.Column(db.Integer,primary_key =True)
    Tarequest_id = db.Column(db.String(200),nullable=False)
    lecture_email =db.Column(db.Integer,nullable=False)
    module_name =db.Column(db.String(200),nullable=False)
    hod_email =db.Column(db.String(200),nullable=False)
    opening_status = db.Column(db.String(200),nullable=False)
    request_statusnum =db.Column(db.Integer,nullable=False)
    request_reason =db.Column(db.String(200),nullable=False)


    def __repr__(self):
        return 'Taopening %r' %self.id

    


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
                
                if user.userrole == 'hod':
                    return redirect(url_for('hoddash'))
                
                if user.userrole == 'lecture':
                    return redirect(url_for('lecturedash'))

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


            dep = Departmenthod.query.all()

            departments = Department.query.all()
            faculties = Faculty.query.all()

            return render_template('admin/departments.html',departments=departments,faculties= faculties,dep=dep)
        
        except:
            return 'The was an issue adding department'



    else:

        dep = Departmenthod.query.all()
        departments =Department.query.all()
        faculties = Faculty.query.all()
        return render_template('admin/departments.html',departments=departments,faculties= faculties,dep=dep)
        






@app.route('/courses',methods=['POST','GET'])
def courses():

    if request.method =='POST':
        name = request.form['name']
        dep_name = request.form['department_name']
        dep_id = 2

        new_course = Course(name =name,department_name = dep_name,department_id=1)

        try:

            db.session.add(new_course)
            db.session.commit()
            departments = Department.query.all()
            courses = Course.query.all()

            return render_template('admin/courses.html',departments=departments,courses=courses)
        
        except:
            return 'The was an issue adding course'



    else:
        departments =Department.query.all()
        courses = Course.query.all()
        return render_template('admin/courses.html',departments=departments,courses= courses)




@app.route('/modules',methods=['POST','GET'])
def modules():

    if request.method =='POST':
        name = request.form['name']
        co_name = request.form['course_name']
        co_id = 2

        new_module = Module(name =name,course_name = co_name,course_id=co_id)

        try:
            db.session.add(new_module)
            db.session.commit()

            courses = Course.query.all()
            modules = Module.query.all()

            return render_template('admin/modules.html',courses = courses , modules = modules)
        
        except:
            return 'The was an issue adding module'



    else:
        modules =Module.query.all()
        courses = Course.query.all()


        return render_template('admin/modules.html',modules = modules, courses = courses)




@app.route('/staff',methods=['POST','GET'])
def staff():

    if request.method =='POST':
        email = request.form['email'].lower()
        password = request.form['password']
        userrole = request.form['userrole']

        new_user = User(email = email, password= password, userrole =  userrole)

        try:
            db.session.add(new_user)
            db.session.commit()

            users = User.query.all()

            return render_template('admin/staff.html',users = users)
        
        except:
            return 'The was an issue adding user'



    else:

        users = User.query.all()
        return render_template('admin/staff.html',users = users)






@app.route('/departmenthods/<id>',methods=['POST','GET'])
def departmenthods(id):

    if request.method =='POST':

        dep_name = request.form['dep_name'].lower()
        dep_id = request.form['dep_id']
        hod_email = request.form['hod_email']

        new_hod = Departmenthod(department_name = dep_name, department_id = dep_id, hod_email = hod_email)

        try:
            db.session.add(new_hod)
            db.session.commit()

            dephods = Departmenthod.query.all()

            return render_template('admin/departmenthods.html',dephods = dephods)
        
        except:
            return 'There was an issue assigning'



    else:

        dep = Department.query.filter_by(id = id).all()
        hods = User.query.filter_by(userrole = 'hod').all()

        return render_template('admin/departmenthods.html',deps = dep, hods= hods)








@app.route('/hoddash',methods=['POST','GET'])
def hoddash():

    if request.method =='POST':

        dep_name = request.form['dep_name'].lower()
        dep_id = request.form['dep_id']
        hod_email = request.form['hod_email']

        new_hod = Departmenthod(department_name = dep_name, department_id = dep_id, hod_email = hod_email)

        try:
            db.session.add(new_hod)
            db.session.commit()

            user = current_user.email

            hodcoz = Departmenthod.query.filter_by(hod_email = user ).first()

            coz = Course.query.filter_by(department_name = hodcoz.department_name ).all()

            tarequests = Tarequest.query.filter_by(hod_email = user).all()

            return render_template('hod/hoddash.html',coz = coz,tarequests = tarequests)
        
        except:
            return 'There was an issue assigning'



    else:
       
       user = current_user.email

       hodcoz = Departmenthod.query.filter_by(hod_email = user ).first()

       coz = Course.query.filter_by(department_name = hodcoz.department_name ).all()

       tarequests = Tarequest.query.filter_by(hod_email = user).all()

       return render_template('hod/hoddash.html',coz = coz, tarequests = tarequests)

    






@app.route('/assignlecturer',methods=['POST','GET'])
def assignlecturer():



    if request.method =='POST':

        uss = User.query.filter_by(id =request.form['lec_id']).first()
        modd = Module.query.filter_by(id = request.form['mod_id'] ).first()

        lec_email = uss.email
        lec_id = request.form['lec_id']
        mod_name = modd.name
        mod_id = request.form['mod_id']




        lec_mod = Modulelecture(module_name = mod_name, module_id = mod_id, lecture_id = lec_id,Lecture_email=lec_email)

        try:
            db.session.add(lec_mod)
            db.session.commit()
            
            url = request.url        
            query_def=parse.parse_qs(parse.urlparse(url).query)['coz'][0]
            cc = query_def

            modlec = Modulelecture.query.all()

            mod = Module.query.filter_by(course_name = cc ).all()

            lecs = User.query.filter_by(userrole ='lecture').all()


            return render_template('hod/assignlecturer.html',modlec = modlec,lecs= lecs,mod = mod)
        
        except:
            return 'There was an issue assigning'



    else:

        url = request.url        
        query_def=parse.parse_qs(parse.urlparse(url).query)['coz'][0]
        cc = query_def
       

        modlec = Modulelecture.query.all()

        mod = Module.query.filter_by(course_name = cc ).all()

        lecs = User.query.filter_by(userrole ='lecture').all()

        return render_template('hod/assignlecturer.html',modlec = modlec,lecs= lecs,mod = mod)








@app.route('/lecturedash',methods=['POST','GET'])
def lecturedash():

    if request.method =='POST':

        user = current_user.email

        dep_name = request.form['dep_name'].lower()
        dep_id = request.form['dep_id']
        hod_email = request.form['hod_email']

        new_hod = Departmenthod(department_name = dep_name, department_id = dep_id, hod_email = hod_email)

        try:
            db.session.add(new_hod)
            db.session.commit()

            user = current_user.email

            modlec = Modulelecture.query.filter_by(Lecture_email = user ).all()



            tarequests = Tarequest.query.filter_by(Lecture_email = user).all()


            return render_template('lecture/lecturedash.html',modlec = modlec,tarequests = tarequests)
        
        except:
            return 'There was an issue assigning'



    else:
       
       user = current_user.email

       tarequests = Tarequest.query.filter_by(Lecture_email = user).all()

       modlec = Modulelecture.query.filter_by(Lecture_email = user ).all()

       return render_template('lecture/lecturedash.html',modlec = modlec,tarequests = tarequests )

    



@app.route('/requestta',methods=['POST','GET'])
def requestta():


    if request.method =='POST':

        cc = request.form['lecmodid']
        recrez = request.form['reason']
        user = current_user.email

        uss = User.query.filter_by(email = user ).first()

        lecid = uss.id
        
        modlec = Modulelecture.query.filter_by(id = cc).first()
        modd = Module.query.filter_by(id = modlec.id).first()
        modname = modd.name
        modid = modd.id

        coz = Course.query.filter_by(id = modd.course_id).first()

        dephod=  Departmenthod.query.filter_by(department_id =coz.department_id).first()

        hodemail = dephod.hod_email

        usz = User.query.filter_by(email =hodemail).first()

        hodid = usz.id

        lec_email = uss.email
        mod_name = modd.name
        recrez = request.form['reason']




        lec_mod = Tarequest(Lecture_email = user, lecture_id = lecid, modulelecture_id = cc,module_name=modname, module_id= modid,hod_email = hodemail,hod_id = hodid, request_status ="request sent", request_statusnum = 1,request_reason =recrez )

        try:
            db.session.add(lec_mod)
            db.session.commit()
            user = current_user.email


            uss = User.query.filter_by(email = user ).first()
            url = request.url        
            query_def=parse.parse_qs(parse.urlparse(url).query)['lecmodid'][0]
            cc = query_def
            modlec = Modulelecture.query.filter_by(id = cc).all()

            return render_template('lecture/requestta.html',modlec = modlec)
        
        except:
            return 'There was an issue assigning'



    else:

        user = current_user.email


        uss = User.query.filter_by(email = user ).first()
        url = request.url        
        query_def=parse.parse_qs(parse.urlparse(url).query)['lecmodid'][0]
        cc = query_def
        modlec = Modulelecture.query.filter_by(id = cc).all()
        lecmodid = cc

        return render_template('lecture/requestta.html',modlec = modlec,lecmodid = lecmodid)




@app.route('/approverequest',methods=['POST','GET'])
def approverequest():

    if request.method =='POST':

        user = current_user.email

        cc = request.form['tarecid']
        recres = request.form['app']


        if recres == "declined":

            tareq = Tarequest.query.filter_by(id =cc).first()

            tareq.request_status ="declined"
            tareq.retuest_statusnum = 30

            try:
                db.session.commit()

                
                taops = Taopening.query.filter_by(module_name = tareq.hod_email).all()

                return render_template('hod/hoddash.html',modlec = modlec, taops = taops)

            except:

                return "couldnt update request"
            
        

        if recres == "approved":

            tareq = Tarequest.query.filter_by(id =cc).first()
            tareq.request_status ="request approved"
            tareq.retuest_statusnum = 2

            le = tareq.Lecture_email
            tarid = tareq.id
            mna = tareq.module_name
            hemail = tareq.hod_email


            try:
                db.session.commit()

                taop = Taopening(lecture_email = le,  Tarequest_id = tarid,   module_name = mna, module_id= modid,hod_email = hemail, opening_status ="Position available", opening_statusnum = 1)
               
                db.session.add(taop)
                
                db.session.commit()


                taops = Taopening.query.filter_by(module_name = tareq.hod_email).all()

                return render_template('hod/hoddash.html',modlec = modlec, taops = taops)

            except:
                return "couldnt update request"


        uss = User.query.filter_by(email = user ).first()

        lecid = uss.id
        modlec = Modulelecture.query.filter_by(id = cc).first()
        modd = Module.query.filter_by(id = modlec.id).first()
        modname = modd.name
        modid = modd.id

        coz = Course.query.filter_by(id = modd.course_id).first()

        dephod=  Departmenthod.query.filter_by(department_id =coz.department_id).first()

        hodemail = dephod.hod_email

        usz = User.query.filter_by(email =hodemail).first()

        hodid = usz.id

        lec_email = uss.email
        mod_name = modd.name
        recrez = request.form['reason']




        lec_mod = Tarequest(Lecture_email = user, lecture_id = lecid, modulelecture_id = cc,module_name=modname, module_id= modid,hod_email = hodemail,hod_id = hodid, request_status ="request sent", request_statusnum = 1,request_reason =recrez )

        try:
            db.session.add(lec_mod)
            db.session.commit()

            user = current_user.email

            uss = User.query.filter_by(email = user ).first()
            url = request.url        
            query_def=parse.parse_qs(parse.urlparse(url).query)['lecmodid'][0]
            cc = query_def
            modlec = Modulelecture.query.filter_by(id = cc).all()
            taops = Taopening.query.filter_by(module_name = tareq.hod_email).all()


            return render_template('hod/approverequest.html',modlec = modlec, taops =taops)
        
        except:
            return 'There was an issue assigning'



    else:

        user = current_user.email


        uss = User.query.filter_by(email = user ).first()
        url = request.url        
        query_def=parse.parse_qs(parse.urlparse(url).query)['tarecid'][0]
        cc = query_def

        tarecid = cc
        
        tarecs = Tarequest.query.filter_by(id = tarecid).first()

        taops = Taopening.query.filter_by(module_name = tarecs.hod_email).all()

    
        return render_template('hod/approverequest.html',tarecs = tarecs,taops = taops)








if __name__ == "__main__":
    app.run(debug = True) 