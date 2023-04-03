from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import pickle

#loading the saved model
with open ('LR_model.pkl', 'rb') as f:
    LR = pickle.load(f)

app = Flask(__name__)
app.secret_key = "secret_key"

# MySQL Configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'telehealth'
mysql = MySQL(app)

#render the LandingPage.html 
@app.route('/')
def home():
	return render_template('LandingPage.html')

@app.route('/homePage')
def homePage():
	return render_template('homePage.html')

@app.route('/signInSignUp', methods = ['GET', 'POST'])
def signInSignUp():
    return render_template('signInSignUp.html')

# User registration page
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO patients (name,email, password) VALUES (%s,%s, %s)', (name, email,password))
        mysql.connection.commit()
        cursor.close()
        return redirect('/signin')

    else:
    	return render_template('signInSignUp.html')



@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM patients WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        if user:
            session['user'] = 'patients'
            return redirect('/homePage') 
    return render_template('/signInSignUp.html')


#predict diabetes based on the user input
@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        BMI = float(request.form['BMI'])
        Age = int(request.form['Age'])
        Insulin = int(request.form['Insulin'])
        Glucose = int(request.form['Glucose'])

        LR_prediction = predict_diabetes(LR, BMI, Age, Insulin, Glucose)

        return render_template('predict.html', LR_prediction=LR_prediction)
    else:
        return redirect('/')

if __name__ == '__main__':
	app.run(debug = True)	