from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import wtforms
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators  import InputRequired, Length, ValidationError

# app = Flask(__name__)

# db= SQLAlchemy()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SECRET_KEY'] ='thisisasecretkey'




db = SQLAlchemy() # db intitialized here
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)



class User(db.Model,UserMixin):
    __tablename__='User'
    id= db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    userrole = db.Column(db.String(50),nullable=False)


class RegisterForm(FlaskForm):
    email = StringField(validators)





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('account/login.html')

@app.route('/register')
def register():
    return render_template('account/register.html')

@app.route('/forget_password')
def forget_password():
    return render_template('account/forget_password.html')





if __name__ == "__main__":
    app.run(debug = True) 