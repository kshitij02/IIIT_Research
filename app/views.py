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
	if session['user_logged_in']==True:
		return render_template('post.html')
	return	redirect(url_for('login'))

@app.route('/timeline')
def timeline():
	if session['user_logged_in']==True:
		return render_template('timeline.html')
	return	redirect(url_for('login'))
	
@app.route('/lab')
def lab():
	if session['user_logged_in']==True:
		return render_template('lab.html')
	return	redirect(url_for('login'))

@app.route('/about')
def about():
	if session['user_logged_in']==True:
		return render_template('about.html')
	return	redirect(url_for('login'))


@app.route('/trending')
def trending():
	if session['user_logged_in']==True:
		return render_template('trending.html')
	return	redirect(url_for('login'))


@app.route('/professor')
def professor():
	if session['user_logged_in']==True:
		return render_template('professor.html')
	return	redirect(url_for('login'))

@app.route('/')	
@app.route('/login')
def login():
	if session['user_logged_in']==True:
		return redirect(url_for('index'))
	return render_template('login.html')

@app.route('/registration')
def registration():
	return render_template('registration.html')

@app.route('/follow')
def follow():
	return insert_follow(email_1,email_2)

def insert_login(id,name,password,type):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	t =(id,name,password,type)
	c=conn.cursor()
	try :
		c.execute("INSERT into login (id,name,password,type) values(?,?,?,?) ", t )
		conn.commit()
		conn.close()
		return True
	except sqlite3.IntegrityError:
		conn.close()
		return "User id already exists"
	#li=c.execute("SELECT * FROM login" )
	#print [l for l in li]

def update_login(id,name,type,password,native,dob):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	t =(name,password,type,native,dob,id)
	c=conn.cursor()
	try :
		c.execute("update login set name=?, password=?,type=?,native=?,dob=? where id=?", t)
		conn.commit()
		conn.close()
		return True
	except sqlite3.IntegrityError:
		conn.close()
		return "User id doesn't exists"
	#li=c.execute("SELECT * FROM login" )
	#print [l for l in li]



def insert_post(student_id,researcharea,lab_id,prof_id,post_text):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
 	conn = sqlite3.connect("project.db")
	conn.text_factory = str
	if session['type']=="professor":
		prof_id=student_id
		student_id=""
		post_person_id=prof_id
	else:
		post_person_id=prof_id
	t =(student_id,researcharea,lab_id,prof_id,post_text,datetime.datetime.now(),post_person_id)
	c=conn.cursor()
	try :
		c.execute("INSERT into post (student_id,researcharea,lab,prof_id,post_text,time,post_person_id) values(?,?,?,?,?,?,?) ", t )
		conn.commit()
		conn.close()
		return True
	except sqlite3.IntegrityError:
		conn.close()
		return "Post cann't be inserted "

def insert_follow(student_id,id_2):
 	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
 	conn.text_factory = str
	t =(student_id,id_2)
	l=(student_id,)
	c=conn.cursor()
	try :
		c.execute("INSERT into follow (following,follower) values(?,?) ", t )
		c.execute("UPDATE login set no_of_followers=no_of_followers+1 where id=?",l)
		conn.commit()
		conn.close()
		return True
	except sqlite3.IntegrityError:
		conn.close()
		return "already exists"


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


def show_post(id):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	conn.text_factory = str
	t=(id,id,)
	c=conn.cursor()
	# li=c.execute("SELECT following FROM follow WHERE follower = ? ", t )
	# li=c.fetchall()
	# # t1=(li,)
 	li=c.execute("SELECT * From post where student_id in (SELECT following FROM follow WHERE follower = ?) or prof_id in (SELECT following FROM follow WHERE follower = ?) ORDER BY time desc",t)
	li=c.fetchall()
	print li
	conn.close()

def list_lab():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
 	li=c.execute("SELECT DISTINCT lab FROM login")
	li=c.fetchall()
	print li
	conn.close()

def list_prof(lab):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	t=(lab,)
 	li=c.execute("SELECT id FROM login where lab=?",t)
	li=c.fetchall()
	print li
	conn.close()


def most_voted_post():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
 	li=c.execute("SELECT * FROM post ORDER BY vote DESC limit 10")
	li=c.fetchall()
	print li
	conn.close()


def most_followed_prof():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
 	li=c.execute("SELECT * FROM login ORDER BY no_of_followers DESC limit 10")
	li=c.fetchall()
	print li
	conn.close()


def most_publications_labs():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
 	li=c.execute("SELECT lab ,COUNT(*) FROM post GROUP BY lab ORDER BY COUNT(*) DESC limit 10  ")
	li=c.fetchall()
	print li
	conn.close()

def timeline_qurrey(id):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	t=(id,)
	l=c.execute("SELECT * login where id=?",t)
	l=c.fetchall()
	type=l[0]
	if type=="student":
 		li=c.execute("SELECT * post where student_id=? ",t)
 	elif type=="professor":
 		li=c.execute("SELECT * post where prof_id=? ",t)
	li=c.fetchall()
	print li
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

def type_find():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	t=(session['userID'],)
	li=c.execute("SELECT type from login where id=? ",t)
	li=c.fetchall()
	# print li
	conn.close()
	return li[0]

@app.route('/loginNext',methods=['POST'])
def loginNext():
	if request.method=='POST':
		id=request.form["id"]
		password=request.form["password"]
		if check_user(id,password)==True:
			session['user_logged_in']=True
			session['userID']=id
			session['type']=type_find()
			return redirect(url_for('index'))
		else :
			# flash( "Invaild credentials!")
			return redirect(url_for('login'))			

@app.route('/logout')
def logout():
	session['user_logged_in']=False
	session.pop('userID',None)
	return render_template('login.html')

@app.route('/read_search',methods=['POST','GET'])
def read_search():
	if request.method=='POST' or request.method=='GET':
		search_name = request.form.get("search_box")
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		db_path = os.path.join(BASE_DIR, "project.db")
		conn = sqlite3.connect(db_path)
		conn.text_factory = str
		t = (search_name,)
		c = conn.cursor()
		li = c.execute("SELECT * FROM login WHERE name =?",t)
		li = c.fetchall()
		if len(li) == 0:
			return "No such person exist"
		else:
			return render_template('search.html',li = li)
		conn.close()	
