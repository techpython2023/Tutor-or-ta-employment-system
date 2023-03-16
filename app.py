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
    isassigned = db.Column(db.Integer,nullable =False)

    def __repr__(self):
        return 'Department %r' %self.id
    

class Course(db.Model):
    __tablename__ ='courses'

    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(200),nullable=False)
    department_name =db.Column(db.String(200),nullable=False)
    department_id = db.Column(db.Integer,nullable=False)
    faculty_name =db.Column(db.String(200),nullable=False)
    faculty_id = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return 'Course %r' %self.id
    

class Module(db.Model):
    __tablename__ ='modules'

    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(200),nullable=False)
    course_name =db.Column(db.String(200),nullable=False)
    course_id = db.Column(db.Integer,nullable=False)
    department_name =db.Column(db.String(200),nullable=False)
    department_id = db.Column(db.Integer,nullable=False)
    faculty_name =db.Column(db.String(200),nullable=False)
    faculty_id = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return 'Module %r' %self.id
    

class Departmenthod(db.Model):
    __tablename__ ='departmenthods'

    id = db.Column(db.Integer,primary_key =True)
    department_name = db.Column(db.String(200),nullable=False)
    department_id =db.Column(db.Integer,nullable=False)
    hod_email =db.Column(db.String(200),nullable=False)
    faculty_name =db.Column(db.String(200),nullable=False)
    faculty_id = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return 'Departmenthod %r' %self.id


class Modulelecture(db.Model):
    __tablename__ ='modulelectures'

    id = db.Column(db.Integer,primary_key =True)
    lecture_email = db.Column(db.String(200),nullable=False)
    module_name =db.Column(db.String(200),nullable=False)
    module_id =db.Column(db.Integer,nullable=False)
    lecture_id =db.Column(db.Integer,nullable=False)
    faculty_name =db.Column(db.String(200),nullable=False)
    faculty_id = db.Column(db.Integer,nullable=False)
    department_name = db.Column(db.String(200),nullable=False)
    department_id =db.Column(db.Integer,nullable=False)
    hod_email =db.Column(db.String(200),nullable=False)
    

    def __repr__(self):
        return 'Modulelecture %r' %self.id
    


class Tarequest(db.Model):
    __tablename__ ='tarequests'

    id = db.Column(db.Integer,primary_key =True)
    lecture_email = db.Column(db.String(200),nullable=False)
    lecture_id =db.Column(db.Integer,nullable=False)
    modulelecture_id =db.Column(db.Integer,nullable=False)
    module_name =db.Column(db.String(200),nullable=False)
    module_id =db.Column(db.Integer,nullable=False)
    hod_email =db.Column(db.String(200),nullable=False)
    hod_id =db.Column(db.Integer,nullable=False)
    request_status =db.Column(db.String(200),nullable=False)
    request_statusnum =db.Column(db.Integer,nullable=False)
    request_reason =db.Column(db.String(8000),nullable=False)
    position_responsibilities = db.Column(db.String(10000),nullable =False)
    course_name =db.Column(db.String(200),nullable=False)
    course_id = db.Column(db.Integer,nullable=False)
    department_name =db.Column(db.String(200),nullable=False)
    department_id = db.Column(db.Integer,nullable=False)
    faculty_name =db.Column(db.String(200),nullable=False)
    faculty_id = db.Column(db.Integer,nullable=False)



    def __repr__(self):
        return 'Tarequest %r' %self.id
    




class Taopening(db.Model):
    __tablename__ ='taopenings'

    id = db.Column(db.Integer,primary_key =True)
    Tarequest_id = db.Column(db.Integer,nullable=False)
    lecture_email =db.Column(db.String(200),nullable=False)
    module_name =db.Column(db.String(200),nullable=False)
    module_id =db.Column(db.Integer,nullable=False)
    hod_email =db.Column(db.String(200),nullable=False)
    opening_status = db.Column(db.String(200),nullable=False)
    opening_statusnum =db.Column(db.Integer,nullable=False)
    position_responsibilities = db.Column(db.String(10000),nullable =False)
    course_name =db.Column(db.String(200),nullable=False)
    course_id = db.Column(db.Integer,nullable=False)
    department_name =db.Column(db.String(200),nullable=False)
    department_id = db.Column(db.Integer,nullable=False)
    faculty_name =db.Column(db.String(200),nullable=False)
    faculty_id = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return 'Taopening %r' %self.id
    


class Positionapplication(db.Model):
    __tablename__ ='positionapplications'

    id = db.Column(db.Integer,primary_key =True)
    Tarequest_id = db.Column(db.Integer,nullable=False)
    lecture_email =db.Column(db.String(200),nullable=False)
    module_name =db.Column(db.String(200),nullable=False)
    module_id =db.Column(db.Integer,nullable=False)
    hod_email =db.Column(db.String(200),nullable=False)
    course_name =db.Column(db.String(200),nullable=False)
    course_id = db.Column(db.Integer,nullable=False)
    department_name =db.Column(db.String(200),nullable=False)
    department_id = db.Column(db.Integer,nullable=False)
    faculty_name =db.Column(db.String(200),nullable=False)
    faculty_id = db.Column(db.Integer,nullable=False)
    applicant_idnumber = db.Column(db.Integer,nullable=False)
    applicant_marks = db.Column(db.Integer,nullable=False)
    applicant_studentnumber = db.Column(db.Integer,nullable=False)
    applicant_idnumber = db.Column(db.Integer,nullable=False)
    applicant_fullnames = db.Column(db.String(200),nullable=False)
    applicant_dutemail = db.Column(db.String(200),nullable=False)
    status = db.Column(db.String(200),nullable=False)
    status_num = db.Column(db.Integer,nullable=False)
    applicant_email =db.Column(db.String(200),nullable=False)
    ratingscrore = db.Column(db.Integer,nullable=False)




    def __repr__(self):
        return 'Positionapplication %r' %self.id
    



class Applicationinterview(db.Model):
    __tablename__ ='applicationinterviews'

    id = db.Column(db.Integer,primary_key =True)
    Tarequest_id = db.Column(db.Integer,nullable=False)
    position_applicationid = db.Column(db.Integer,nullable=False)
    lecture_email =db.Column(db.String(200),nullable=False)
    module_name =db.Column(db.String(200),nullable=False)
    module_id =db.Column(db.Integer,nullable=False)
    hod_email =db.Column(db.String(200),nullable=False)
    applicant_dutemail = db.Column(db.String(200),nullable=False)
    status = db.Column(db.String(200),nullable=False)
    status_num = db.Column(db.Integer,nullable=False)
    applicant_email =db.Column(db.String(200),nullable=False)
    venue =db.Column(db.String(200),nullable=False)
    datetime = db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return 'Applicationinterview %r' %self.id
    



class Tarating(db.Model):
    __tablename__ ='taratings'

    id = db.Column(db.Integer,primary_key =True)
    Tarequest_id = db.Column(db.Integer,nullable=False)
    position_applicationid = db.Column(db.Integer,nullable=False)
    lecture_email =db.Column(db.String(200),nullable=False)
    module_name =db.Column(db.String(200),nullable=False)
    module_id =db.Column(db.Integer,nullable=False)
    hod_email =db.Column(db.String(200),nullable=False)
    applicant_email =db.Column(db.String(200),nullable=False)
   

    def __repr__(self):
        return 'Tarating %r' %self.id

    


@app.route('/',methods=['POST','GET'])
def index():

    taops = Taopening.query.filter_by(opening_statusnum = 1).all()

    return render_template('index.html',taops = taops)


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

    ops = Taopening.query.all() 


    return render_template('admin/admin.html',ops= ops)










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
        faculty_id = request.form['faculty_id']

        fac = Faculty.query.filter_by(id = faculty_id).first()

        facname = fac.name


        new_department = Department(name =name,faculty_name = facname, faculty_id = faculty_id,isassigned =1)

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
        dep_id = request.form['department_id']

        dep = Department.query.filter_by(id = dep_id).first()

        depname = dep.name
        facname = dep.faculty_name
        facid = dep.faculty_id 

        new_course = Course(name =name,department_name = depname,department_id=dep_id, faculty_name = facname, faculty_id = facid)

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
        co_id = request.form['course_id']

        coz = Course.query.filter_by(id = co_id).first()

        coname = coz.name
        depname =  coz.department_name
        depid = coz.department_id
        facname = coz.faculty_name
        facid = coz.faculty_id


        new_module = Module(name =name,course_name = coname,course_id=co_id,department_name = depname,department_id = depid,faculty_name = facname, faculty_id = facid)

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

        dep1 = Department.query.filter_by(id = dep_id).first()

        facname = dep1.faculty_name
        facid = dep1.faculty_id


        new_hod = Departmenthod(department_name = dep_name, department_id = dep_id, hod_email = hod_email,faculty_name =facname, faculty_id = facid)

        try:
            db.session.add(new_hod)
            db.session.commit()

            dep = Department.query.filter_by(id = dep_id).first()
            dep.isassigned = 2
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

            coz = Course.query.filter_by(department_id = hodcoz.department_id ).all()

            tarequests = Tarequest.query.filter_by(hod_email = user).all()

            taops = Taopening.query.filter_by(hod_email = user).all()


            return render_template('hod/hoddash.html',coz = coz,tarequests = tarequests, taops = taops)
        
        except:
            return 'There was an issue assigning'



    else:
       
       user = current_user.email

       dephod = Departmenthod.query.filter_by(hod_email = user ).first()

       coz = Course.query.filter_by(department_id = dephod.department_id ).all()

       tarequests = Tarequest.query.filter_by(hod_email = user).all()
       taops = Taopening.query.filter_by(hod_email = user).all()
       inters = Applicationinterview.query.all()


       return render_template('hod/hoddash.html',coz = coz, tarequests = tarequests,taops = taops, inters = inters)

    






@app.route('/assignlecturer',methods=['POST','GET'])
def assignlecturer():



    if request.method =='POST':

        uss = User.query.filter_by(id = request.form['lec_id']).first()
        modd = Module.query.filter_by(id = request.form['mod_id'] ).first()

        lecemail = uss.email
        lecid = request.form['lec_id']
        modname = modd.name
        modid = modd.id
        facname = modd.faculty_name
        facid = modd.faculty_id
        depname = modd.department_name
        depid = modd.department_id
        dephod = Departmenthod.query.filter_by(department_id =depid).first()
        hodemail = dephod.hod_email



        lec_mod = Modulelecture(lecture_email =lecemail ,module_name = modname, module_id =modid,lecture_id = lecid,faculty_name = facname,faculty_id = facid,department_id = depid, department_name = depname,hod_email =hodemail)

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

       us = User.query.filter_by(email = user).first()

       tarequests = Tarequest.query.filter_by(lecture_email = user).all()

       modlec = Modulelecture.query.all()

       return render_template('lecture/lecturedash.html',modlec = modlec,tarequests = tarequests )

    



@app.route('/requestta',methods=['POST','GET'])
def requestta():


    if request.method =='POST':

        lecmodid = request.form['lecmodid']
        recrez = request.form['reason']
        recpozres = request.form['posres']
        user = current_user.email

        uss = User.query.filter_by(email = user ).first()

        lecid = uss.id
        
        modlec = Modulelecture.query.filter_by(id = lecmodid).first()
        modname = modlec.module_name
        modid = modlec.module_id
        lecid = uss.id
        modlecid = modlec.id
        hodemail = modlec.hod_email
        us1 = User.query.filter_by(email = hodemail).first()
        hodid = us1.id
        cz = Module.query.filter_by(id = modid).first()
        cozname = cz.course_name
        cozid= cz.course_id

        depname = modlec.department_name
        depid = modlec.department_id 

        facid = modlec.faculty_id
        facname = modlec.faculty_name

        





        lec_mod = Tarequest(lecture_email = user, lecture_id = lecid, modulelecture_id =modlecid,module_name=modname, module_id= modid,hod_email = hodemail,hod_id = hodid, request_status ="request sent", request_statusnum = 1,request_reason =recrez,position_responsibilities = recpozres, course_name =cozname, course_id = cozid,department_id = depid, department_name = depname, faculty_id = facid, faculty_name =facname)

        try:
            db.session.add(lec_mod)
            db.session.commit()
            user = current_user.email


            uss = User.query.filter_by(email = user ).first()
            
            modlec = Modulelecture.query.filter_by(id = modlecid).all()

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

            le = tareq.lecture_email
            tarid = tareq.id
            mna = tareq.module_name
            hemail = tareq.hod_email
            reqrezzz = tareq.request_reason
            modid = tareq.module_id
            posres = tareq.position_responsibilities
            cozid = tareq.course_id
            cozname = tareq.course_name
            depid = tareq.department_id
            depname = tareq.department_name
            facname = tareq.faculty_name
            facid = tareq.faculty_id



            # try:
            db.session.commit()

            taop = Taopening(lecture_email = le,  Tarequest_id = tarid,   module_name = mna,module_id =modid,hod_email = hemail, opening_status ="Position available", opening_statusnum = 1,position_responsibilities = posres, course_name= cozname,course_id= cozid, department_name =depname, department_id =depid,faculty_name = facname, faculty_id = facid)
            
            db.session.add(taop)

            db.session.commit()


            taops = Taopening.query.filter_by(module_name = tareq.hod_email).all()

            return render_template('hod/hoddash.html',taops = taops)

            # except:
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
    

@app.route('/positiondetails',methods=['POST','GET'])
def positiondetails():


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



        url = request.url        
        query_def=parse.parse_qs(parse.urlparse(url).query)['posid'][0]
        cc = query_def
        pos = Taopening.query.filter_by(id = cc).first()
        lecmodid = cc

        hodemail = pos.hod_email


        dephod=  Departmenthod.query.filter_by(hod_email = hodemail).first()

        dephodid = dephod.department_id

        dep = Department.query.filter_by(id = dephodid).first()

        depname = dep.name
        facname = dep.faculty_name
        cozname = pos.course_name 
        res = pos.position_responsibilities








        return render_template('positiondetails.html',pos= pos,depname =depname,facname = facname,cozname= cozname,res =res)







@app.route('/apply',methods=['POST','GET'])
@login_required
def apply():

    if request.method =='POST':

        posid = request.form['opid']

        pos = Taopening.query.filter_by(id = posid).first()

        mark = request.form['mark']
        stnum = request.form['stnum']
        idnum = request.form['idnum']
        fullname = request.form['fullname']
        dutemail = request.form['dutemail'].lower()
        user = current_user.email
        
        

        pos_app = Positionapplication(Tarequest_id = pos.id,lecture_email = pos.lecture_email, module_name = pos.module_name, module_id = pos.module_id,hod_email = pos.hod_email, course_name = pos.course_name,course_id = pos.course_id,department_name = pos.department_name, department_id = pos.department_id,faculty_name = pos.faculty_name, faculty_id = pos.faculty_id,applicant_idnumber =idnum, applicant_marks = mark ,applicant_studentnumber = stnum,applicant_fullnames = fullname,applicant_dutemail = dutemail,status = 'application received',status_num =1,applicant_email = user )

        try:
            db.session.add(pos_app)
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



        url = request.url        
        query_def=parse.parse_qs(parse.urlparse(url).query)['posid'][0]
        cc = query_def
        pos = Taopening.query.filter_by(id = cc).first()
        
        return render_template('apply.html',pos= pos)
    




@app.route('/tutordash',methods=['POST','GET'])
def tutordash():

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

            modlec = Modulelecture.query.filter_by(lecture_email = user ).all()



            tarequests = Tarequest.query.filter_by(lecture_email = user).all()
            


            return render_template('tutor/tutordash.html',modlec = modlec,tarequests = tarequests)
        
        except:
            return 'There was an issue assigning'



    else:
       
       user = current_user.email

       us = User.query.filter_by(email = user).first()

       posapps = Positionapplication.query.filter_by(applicant_email = user).all() 
       tarequests = Tarequest.query.filter_by(lecture_email = user).all()

       modlec = Modulelecture.query.all()
       inters = Applicationinterview.query.filter_by(applicant_email = user).all()


       return render_template('tutor/tutordash.html',modlec = modlec,tarequests = tarequests, posapps = posapps, inters =inters )

    



@app.route('/positionapps',methods=['POST','GET'])
def positionapps():
       
       posapps = Positionapplication.query.all()
    


       return render_template('hod/positionapps.html',posapps = posapps)

   






@app.route('/scheduleinterview',methods=['POST','GET'])
def scheduleinterview():

    if request.method =='POST':

        user = current_user.email
        appid = request.form['appid']
        venue = request.form['venue']
        datetime = request.form['date']

        posapp = Positionapplication.query.filter_by(id = appid).first()

        app_inter = Applicationinterview(Tarequest_id = posapp.Tarequest_id,position_applicationid = posapp.id,lecture_email= posapp.lecture_email,module_name = posapp.module_name,module_id= posapp.module_id,hod_email = posapp.hod_email, applicant_dutemail = posapp.applicant_dutemail,status ='interview secheduled',status_num =1,applicant_email =posapp.applicant_email,venue=venue, datetime =datetime)

        # try:
        db.session.add(app_inter)
        db.session.commit()

        user = current_user.email

        modlec = Modulelecture.query.filter_by(lecture_email = user ).all()

        tarequests = Tarequest.query.filter_by(lecture_email = user).all()

        return render_template('hod/hoddash.html',modlec = modlec,tarequests = tarequests)
        
        # except:
        return 'There was an issue assigning'


    else:
       
       user = current_user.email

       us = User.query.filter_by(email = user).first()

       url = request.url        
       query_def=parse.parse_qs(parse.urlparse(url).query)['appid'][0]
       cc = query_def
       posapp = Positionapplication.query.filter_by(id = cc).first() 
       return render_template('hod/scheduleinterview.html',posapp = posapp)





    










if __name__ == "__main__":
    app.run(debug = True) 