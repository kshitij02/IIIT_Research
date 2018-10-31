from flask import render_template
from flask import url_for,redirect
from flask import request
import sqlite3
import os.path

# Imported a function to render templates

from app import app

@app.route('/')
@app.route('/main')
def index():
	user = {'nickname': 'Mitesh'}
	return render_template('stud.html',title='Student',user=user)
	
@app.route('/login')
def login():
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
		return "User inserted"
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
		return "No such User exists"
	else :
		return str(li)
	conn.close()

@app.route('/registrationNext',methods=['POST'])
def registrationNext():
	if request.method=='POST' :
		id=request.form["id"]
		name=request.form["name"]
		password=request.form["password"]
		type=request.form["type"]
		return insert_login(id,name,password,type)

@app.route('/loginNext',methods=['POST'])
def loginNext():
	if request.method=='POST':
		id=request.form["id"]
		password=request.form["password"]
		return check_user(id,password)

# @app.route('/loginNext',methods=['GET','POST'])
# def loginNext():
# 	# To find out the method of request, use 'request.method'
# 	if request.method == "POST":
# 		print request.args
# 		userID = request.args.get("id")
# 		password = request.args.get("password")
# 		# Can perform some password validation here
# 		return "Login Successful for: %s" % userID

