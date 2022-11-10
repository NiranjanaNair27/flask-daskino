from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt as sa
from functools import wraps
import random

app = Flask(__name__)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:niru123@localhost/daskino'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'awwfaw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def index():
    return render_template('homepage.html')

@app.route('/register')
def register():
    return render_template('homepage.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/bookingtheatre')
def bookingtheatre():
    return render_template('bookingtheatre.html')

@app.route('/contact')
def contact():
    return render_template('contactus.html')

# @app.route("/login", methods = ['GET', 'POST'])
# def logincustomer():
#     if request.method == 'POST':
#         usercust = request.form['username']
#         password_candidate = request.form['password']
#         user = db.session.query(CustomerDet).filter(CustomerDet.username == usercust).first()
#         db.session.commit()
#         if user is None:
#             flash('No such username exists', 'danger')
#             return render_template('login.html')
#         else:
#             if sa.verify(password_candidate, user.password):
#                 session['logged_in'] = True
#                 session['username'] = usercust
#                 session['type'] = 'C'
#                 session['name'] = user.namecust
#                 session['pincode'] = user.pincode
#                 flash('You are now logged in', 'success')
#                 return redirect(url_for('home'))
#             else:
#                 flash('Incorrect password', 'danger')
#                 return render_template('locust.html')
#     else:
#         return render_template('login.html')

@app.route('/offers')
def offers():
    return render_template('offers.html')

# @app.route('/trans')
# def trans():
#     return render_template('transactions.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('UNAUTHORISED, Please Login', 'danger')
            return redirect(url_for('home'))
    return wrap

def username_predict(u, t):
    c = True
    while c:
        if not db.session.query(t).filter(t.username == u).count() == 0:
            x = random.randint(0, 6000)
            u += str(x)
            s = ". Try " + u
            c = False
    return s

@app.route("/register", methods = ['GET', 'POST'])
def registerhospital():
    if request.method == 'POST':
        namecust = request.form['namecust']
        username = request.form['username']
        password = sa.hash(request.form['password'])
        phonenum = request.form['phonenum']
        if db.session.query(UserDet).filter(UserDet.username == username).count() == 0:
            data = UserDet(namecust, username, password, phonenum)
            db.session.add(data)
            db.session.commit()
            flash('you are now registered', 'success')
            return redirect(url_for('loginhospital'))
        else:
            flash("Username already exists" + username_predict(username, UserDet), 'danger')
    return render_template('remnmg.html')

# models

# class administration(db.Model):
#     admin_id=db.IntegerField(primary_key=True)
#     theatre_id4=db.ForeignKey(theatre,on_delete=db.CASCADE)
#     username=db.CharField(max_length=30)
#     password=db.CharField(max_length=20)
#     salary=db.IntegerField()

class UserDet(db.Model):  # type: ignore
    __tablename__ = 'userdetails'
    userid = db.Column(db.Integer, primary_key = True)
    namecust = db.Column(db.String(200))
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(300))
    phonenum = db.Column(db.String(10))


    def __init__(self, namecust, username, password, phonenum):
        self.namecust = namecust
        self.username = username
        self.password = password
        self.phonenum = phonenum 


# class movies(db.Model):
#     __tablename__='movies'
#     moviename = db.Column(db.String(200), primary_key=True)
#     description= db.column(db.text())
#     genre= db.column(db.string(20))
#     rating=db.column(db.string(5))

#     def __init__(self, description, genre, rating):
#         self.description=description
#         self.genre=genre
#         self.rating=rating

# class theatres(db.Model):
#     __tablename__='theatres'
#     theatreid=db.column(db.Integer, primary_key= True)
#     theatrename=db.Column(db.String(200))
#     morning_show=db.column(db.String(200), db.ForeignKey('movies.moviename'))
#     movies= db.relationship('movies',backref=backref("movies",  uselist=False))
#     evening_show=db.column(db.string(200))

# class tickets(db.Model):
#     __tablename__='tickets'
#     ticketid=db.column(db.Integer, primary_key= True)
    
if __name__ == '__main__':
    app.run()