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
from flask import render_template
from flask import url_for,redirect,session
from flask import request
from datetime import datetime
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
		lis=list_following()
		posts=show_post()
		return render_template('index.html',id=session['userID'],lis=lis,posts=posts)
	return	redirect(url_for('login'))

@app.route('/timeline')
def timeline():
	if session['user_logged_in']==True:
		posts=show_timeline(session['userID'])
		# return str(len(posts))
		return render_template('timeline.html',id=session['userID'],posts=posts)
	return	redirect(url_for('login'))
	
@app.route('/lab')
def lab():
	if session['user_logged_in']==True:
		return render_template('lab.html',id=session['userID'])
	return	redirect(url_for('login'))

@app.route('/about/<id>')
def about(id):
	if session['user_logged_in']==True:
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		db_path = os.path.join(BASE_DIR, "project.db")
		conn = sqlite3.connect(db_path)
		conn.text_factory = str
		c=conn.cursor()
		names=(id,)
		t=(session['userID'],id,)
		li=c.execute("SELECT * FROM follow WHERE follower = ? and following=?" , t )
		li=c.fetchall()
		followed=1
		if len(li) == 0 :
			followed=0
		lin=c.execute("SELECT name,type,native,dob,id FROM login WHERE id= ?",names)
		lin=c.fetchall()
		lis=list_follower(id)
		posts=show_timeline(id)
		for li in lin:
			return render_template('about.html',id=session['userID'],li=li,followed=followed,lis=lis,posts=posts)
	return	redirect(url_for('login'))


@app.route('/trending')
def trending():
	if session['user_logged_in']==True:
		return render_template('trending.html',id=session['userID'])
	return	redirect(url_for('login'))


@app.route('/professor')
def professor():
	if session['user_logged_in']==True:
		return render_template('professor.html',id=session['userID'])
	return	redirect(url_for('login'))

@app.route('/')	
@app.route('/login')
def login():
	if session['user_logged_in']==True:
		return redirect(url_for('index',id=session['userID']))
	return render_template('login.html')

@app.route('/registration')
def registration():
	return render_template('registration.html')

@app.route('/follow/<id2>')
def follow(id2):
	return insert_follow(id2=id2,id1=session['userID'])


def list_following():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	t=(session['userID'],)
 	li=c.execute("SELECT name,id from login where id IN (SELECT following FROM follow where follower=?)",t)
	li=c.fetchall()
	conn.close()
	return li

def list_follower(id):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	t=(id,)
 	li=c.execute("SELECT name,id from login where id IN (SELECT follower FROM follow where following=?)",t)
	li=c.fetchall()
	conn.close()
	return li 
	
def insert_login(id,name,password,type,lab):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	t =(id,name,password,type,lab)
	c=conn.cursor()
	try :
		c.execute("INSERT into login (id,name,password,type,lab) values(?,?,?,?,?) ", t )
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


@app.route('/insert_post',methods=['POST'])
def insert_post():
	if request.method=='POST' :
		researcharea=request.form['research_area']
		lab_id=request.form.get('lab')
		prof_id=request.form.get('prof')
		post_text=request.form.get('post_content')
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		db_path = os.path.join(BASE_DIR, "project.db")
		conn = sqlite3.connect(db_path)
	 	conn.text_factory = str
		if session['type']=="professor":
			prof_id=session['userID']
			student_id=""
			post_person_id=prof_id
		else:
			post_person_id=session['userID']
			student_id=session['userID']
		t =(student_id,researcharea,lab_id,prof_id,post_text,datetime.now(),post_person_id,0)
		c=conn.cursor()
		try :
			c.execute("INSERT into post (student_id,researcharea,lab,prof_id,post_text,time,post_person_id,vote_count) values(?,?,?,?,?,?,?,?) ", t )
			conn.commit()
			conn.close()
			return redirect(url_for('index'))
		except sqlite3.IntegrityError:
			conn.close()
			return "Post can't be inserted "


def insert_follow(id2,id1):
 	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
 	conn.text_factory = str
	t =(id2,id1)
	l=(id2,)
	c=conn.cursor()
	print id1,id2
	try :
		c.execute("INSERT into follow (following,follower) values(?,?) ", t )
		c.execute("UPDATE login set no_of_followers=no_of_followers+1 where id=?",l)
		conn.commit()
		conn.close()
		return redirect(url_for('about',id=id2))
	except sqlite3.IntegrityError:
		conn.close()
		return redirect(url_for('about',id=id2))


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

def show_post():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	t=(session['userID'],)
	c=conn.cursor()
 	li=c.execute("SELECT * From post where post_person_id in (SELECT following FROM follow WHERE follower = ?) ORDER BY time desc",t)
	li=c.fetchall()
	conn.close()
	return li


def show_timeline(id):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	t=(id,)
	c=conn.cursor()
 	li=c.execute("SELECT * From post where post_person_id = ? ORDER BY time desc",t)
	li=c.fetchall()
	conn.close()
	return li


def list_lab():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
 	li=c.execute("SELECT DISTINCT lab FROM login where lab!=None")
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



def increase_vote_count(id,post_id):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	t=(post_id,)
	t1=(post_id,id)
	c.execute("UPDATE post set vote_count=vote_count+1 where post_id=?",t)
	c.execute("INSERT into vote_table (post_id,voted_person_id) values (?,?) ", t1 )
	conn.commit()
	conn.close()
	


@app.route('/registrationNext',methods=['POST'])
def registrationNext():
	if request.method=='POST' :
		id=request.form["id"]
		name=request.form["name"]
		password=request.form["password"]
		type=request.form["type"]
		if type=="student":
			lab=""
		elif type=="professor":
			lab=request.form["lab"]
		if insert_login(id,name,password,type,lab)==True:
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
			return redirect(url_for('index',id=session['userID']))
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
