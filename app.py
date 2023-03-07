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


@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html')


@app.route('/login',methods= ['POST', 'GET'])
def login():


    if request.method =='POST':
        user_email = request.form['email']
        user_password = request.form['password']
        user = User.query.filter_by(email = user_email).first()
        
        if user:
            if user.password == user_password:

                login_user(user)
                return redirect(url_for('index'))
        
    else:
        return render_template('account/login.html')




@app.route('/register',methods=['POST','GET'])
def register():

    if request.method =='POST':
        user_email = request.form['email']
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





if __name__ == "__main__":
    app.run(debug = True) 