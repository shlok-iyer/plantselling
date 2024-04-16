from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app=Flask(__name__)
app.secret_key ='xyzsdfg'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123!'
app.config['MYSQL_DB'] = 'users'
mysql=MySQL(app)

@app.route('/')

@app.route('/login', methods =['GET', 'POST'])


def login():
    message=''
    if request.method=='POST' and 'email' in request.form and 'password' in request.form:
        email=request.form['email']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM USER WHERE email=%s AND password=%s ",(email,password))
        user = cursor.fetchone()
        if user: 
            session['loggedin'] = True
            session['userid']=user['userid']
            session['email']=user['email']
            session['name']=user['name']
            session['address']=user['address']
            message = 'Logged in successfully !'
            #return render_template('index.html', message = message)
            return redirect(url_for('index'))
        else:
            message='Please enter the correct credentials'
    return render_template('loginnew.html',message=message)
@app.route('/logout')
def logout():
    session.pop('name',None)
    session.pop('userid', None)
    session.pop('email', None)
    session.pop('address',None)
    return redirect(url_for('login'))
@app.route('/register',methods=['GET','POST'])
def register():
    message=''
    if request.method=='POST' and 'email' in request.form and 'name' in request.form and 'address' in request.form :
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        address=request.form['address']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account=cursor.fetchone()
        if account:
            message = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        elif not name or not password or not email:
            message = 'Please fill out the form !'
        else:
            cursor.execute("INSERT INTO user VALUES (NULL, % s, % s, % s,%s)",(name,email,address,password,))
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('registernew.html', message = message)
@app.route('/cart')
def cart():
    return render_template("cartindex.html")
@app.route('/index')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
 
