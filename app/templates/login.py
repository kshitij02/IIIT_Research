import sqlite3


def insert_login(id,name,password,type):
	conn = sqlite3.connect('project.db')
	conn.text_factory = str
	t =(id,name,password,type)
	c=conn.cursor()
	try :
		c.execute("INSERT into login values(?,?,?,?) ", t )
		conn.commit()
	except sqlite3.IntegrityError:
		return "User id already exists"
	#li=c.execute("SELECT * FROM login" )
	#print [l for l in li]
	conn.close()
def check_user(id,password):
	conn = sqlite3.connect('project.db')
	conn.text_factory = str
	t =(id,password)
	c=conn.cursor()
	li=c.execute("SELECT * FROM login WHERE id = ? and password=?" , t )
	li=c.fetchall()
	if len(li) == 0 :
		return "No such User exists"
	else :
		return li
	conn.close()


if __name__ == '__main__':
	insert_login("12","sivangi","si","student")
	check_user('12','si')
