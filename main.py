from flask import Flask, render_template, request
import mysql.connector 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        mydb = mysql.connector.connect(
            host = 'remotemysql.com',
            user = 'Rz8hqldk4',
            password = 'nd0wK03xe0',
            database = 'Rz8hqnldk4'
        )

        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT * FROM LoginDetails WHERE Name = %s AND Password = %s",
            (username, password)
        )
        account = mycursor.fetchone()

        mycursor.close()
        mydb.close()

        if account:
            name = account[1]
            id = account[0]
            msg = 'Logged in Successfully'
            return render_template('index.html',msg=msg, name=name, id=id)
        else:
            msg = 'Incorrect Credentials'

    return render_template('index.html', msg=msg)

@app.route('/register',methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        mydb = mysql.connector.connect(
            host = 'remotemysql.com',
            user = 'Rz8hqldk4',
            password = 'nd0wK03xe0',
            database = 'Rz8hqnldk4'
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM LoginDetails WHERE Name = %s",(username))
        account = mycursor.fetchone()

        if account:
            msg = "Account already exists"
        else:
            mycursor.execute(
                "INSERT INTO LoginDetails (Name, Password, Email) VALUES (%s, %s, %s)",
                (username, password, email)
            )
            mydb.commit()
            msg = "Successful registered"

        mycursor.close()
        mydb.close()

    return render_template('register.html', msg=msg)

@app.route('/logout')
def logout():
    msg = 'Logged out successfully'
    return render_template('index.html', msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)