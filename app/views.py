from flask import render_template
from flask import url_for,redirect,session
from flask import request
import sqlite3
import os.path
# from flask import Flask, session
# from flask.ext.session import Session
# from flask.ext.session import Session


# Imported a function to render templates

from app import app

app.secret_key = "Ramukaka"
 
# app = Flask(__name__)

# @app.route('/main')
# def index():
# 	user = {'nickname': 'Mitesh'}
# 	return render_template('stud.html',title='Student',user=user)

# session[userlogedin]=False
# session = Session()
# session[user_logged_in]=False
@app.route('/index')
def index():
	if session['user_logged_in']==True:
		return render_template('index.html')
	return	redirect(url_for('login'))
@app.route('/post')
def post():
	return render_template('post.html')

@app.route('/timeline')
def timeline():
	return render_template('timeline.html')

@app.route('/lab')
def lab():
	return render_template('lab.html')

@app.route('/')	
@app.route('/login')
def login():
	if session['user_logged_in']==True:
		return redirect(url_for('index'))
	return render_template('login.html')

@app.route('/registration')
def registration():
	return render_template('registration.html')

def insert_login(id,name,password,type):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	t =(id,name,password,type)
	c=conn.cursor()
	try :
		c.execute("INSERT into login values(?,?,?,?) ", t )
		conn.commit()
		conn.close()
		return True
	except sqlite3.IntegrityError:
		conn.close()
		return "User id already exists"
	#li=c.execute("SELECT * FROM login" )
	#print [l for l in li]
	


def check_user(id,password):

	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	t =(id,password)
	c=conn.cursor()
	li=c.execute("SELECT * FROM login WHERE id = ? and password=?" , t )
	li=c.fetchall()
	if len(li) == 0 :
		return "Invaild credentials!"
	else :
		return True
	conn.close()

@app.route('/registrationNext',methods=['POST'])
def registrationNext():
	if request.method=='POST' :
		id=request.form["id"]
		name=request.form["name"]
		password=request.form["password"]
		type=request.form["type"]
		if insert_login(id,name,password,type)==True:
			return redirect(url_for('login'))
		# flash("User id already Exits!!")
		return redirect(url_for('registration'))

@app.route('/loginNext',methods=['POST'])
def loginNext():
	if request.method=='POST':
		id=request.form["id"]
		password=request.form["password"]
		if check_user(id,password)==True:
			session['user_logged_in']=True
			session['userID']=id
			return redirect(url_for('index'))
		else :
			# flash( "Invaild credentials!")
			return redirect(url_for('login'))			

@app.route('/logout')
def logout():
	session['user_logged_in']=False
	session.pop('userID',None)
	return render_template('login.html')

# @app.route('/loginNext',methods=['GET','POST'])
# def loginNext():
# 	# To find out the method of request, use 'request.method'
# 	if request.method == "POST":
# 		print request.args
# 		userID = request.args.get("id")
# 		password = request.args.get("password")
# 		# Can perform some password validation here
# 		return "Login Successful for: %s" % userID

