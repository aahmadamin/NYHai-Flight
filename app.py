from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
app = Flask(__name__)
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='flight_booking',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
@app.route('/')
def main():
	return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
	
	email = request.form['inputEmail']
	password = request.form['inputPassword']
	name = request.form['inputName']
	passport_country = request.form['Country']
	Pass_exp = request.form['inputPass_exp']
	pass_num = request.form['inputPass_num']
	dob = request.form['inputDOB']
	state = request.form['inputState']
	city = request.form['inputCity']
	street = request.form['inputStreet']
	building = request.form['building']
	phone = request.form['inputPhone']

	cursor = conn.cursor()
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute (query, (email))
	data=cursor.fetchone()
	error = None

	if(data):
		error = "This user already exists"
		return render_template('signup.html')
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, )'
		cursor.execute(ins, (email, name, password, building, street, city, state, phone, pass_num, Pass_exp, passport_country, dob))

		conn.commit()
		cursor.close()
		return render_template('index.html')


	@app.route('/showLogin')
	def login_page():
		return render_template('login.html')

	@app.route('/SignIn')
	def SignIn():
		email = request.form['Sign_email']
		password = request.form['Sign_password']
		cursor = conn.cursor()
		query = 'SELECT password FROM customer WHERE email = %s password=%s'
		cursor.execute (query, (email, password))

		data=cursor.fetchone()
		cursor.close()
		error = None
		print(data)
		if (data):

			return render_template('home.html', user=email)

		else:
			error = 'Invalid login or username'
			return render_template('login.html', error=error)



	

if __name__ == "__main__":
    app.run()