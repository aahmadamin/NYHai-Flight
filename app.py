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

@app.route('/showUsertype')
def ShowUsertype():

	return render_template('signup_usertype.html')
@app.route('/Usertype_redirect', methods=['POST'])
def Usertype_redirect():
	user = request.form['type_user']
	if user == 'Customer':
		return render_template('signup_customer.html')
	elif user == 'Airline Staff':
		return render_template('signup_airlinestaff.html')
	else:
		return render_template('signup_bookingagent.html')
	# return render_template('signup_customer.html')

@app.route('/showLogin', methods=['GET', "POST"])
def showLogin():
	return render_template('login.html')

@app.route('/Login', methods=['GET', "POST"])
def Login():
	type_user = request.form['type_user']
	email = request.form['Sign_email']
	password = request.form['Sign_password']
	cursor = conn.cursor()

	if type_user == 'Customer':
		query = "SELECT * FROM customer WHERE email = %s and password = %s"
		cursor.execute(query, (email, password))
		data = cursor.fetchone()
		cursor.close()
		error=None
		if(data):
			session['email'] = email
			return redirect(url_for('profileCustomer'))
		else:
			error = 'Invalid login or password'
			return render_template('login.html', error=error)
	elif type_user=='Booking Agent':
		query = 'SELECT * FROM booking_agent WHERE email = %s and password = %s'
		cursor.execute(query, (email, password))
		data = cursor.fetchone()
		cursor.close()
		error=None
		if(data):
			session['email'] = email
			return redirect(url_for('home_agent.html'))
		else:
			error = 'Invalid login or password'
			return render_template('login.html', error=error)
	elif type_user=='Airline Staff':
		query = 'SELECT * FROM airline_staff WHERE email = %s and password = %s'
		cursor.execute(query, (email, password))
		data = cursor.fetchone()
		cursor.close()
		error=None
		if(data):
			session['email'] = email
			return redirect(url_for('home_staff.html'))
		else:
			error = 'Invalid login or password'
			return render_template('login.html', error=error)




@app.route('/showSignUpCustomer')
def showSignUpCustomer():

	return render_template('signup_customer.html')

@app.route('/ShowSignUpStaff')
def ShowSignUpStaff():
	return render_template('signup_staff.html')

@app.route('/ShowSignUpAgent')
def ShowSignUpAgent():
	return render_template('signup_agent.html')

@app.route('/signUpAgent', methods=['GET', 'POST'])
def signUpAgent():
	email = request.form['email']
	passw = request.form['password']
	agentid = request.form['agentid']

	cursor = conn.cursor()
	query = 'SELECT * FROM booking_agent WHERE email = %s'
	cursor.execute (query, (email))
	data=cursor.fetchone()
	error = None
	if(data):
		error = "This user already exists"
		#debug
		return render_template('signup_bookingagent.html')
	else:
		ins = 'INSERT INTO booking_agent(email, password, booking_agent_id) VALUES(%s, %s, %s)'
		

		cursor.execute(ins, (email, passw, agentid))
		conn.commit()
		cursor.close()
		return render_template('signin.html')

@app.route('/signUpStaff', methods=['GET', 'POST'])
def signUpStaff():
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	dob = request.form['dob']
	airline = request.form['airline']
	cursor = conn.cursor()
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute (query, (username))
	data=cursor.fetchone()
	error = None
	if(data):
		error = "This user already exists"
		#debug
		return render_template('signup_staff.html')
	else:
		ins = 'INSERT INTO airline_staff(username, password, first_name, last_name, dob, airline_staff) VALUES(%s, %s, %s, %s, %s, %s)'
		

		cursor.execute(ins, (username, password, first_name, last_name, dob, airline_staff))
		conn.commit()
		cursor.close()
		return render_template('signin.html')

@app.route('/signUpCustomer', methods=['GET','POST'])
def signUpCustomer():
	email = request.form['inputEmail']
	password = request.form['inputPassword']
	name = request.form['inputName']
	date = request.form['dob']
	building = request.form['building']
	street = request.form['inputStreet']
	city = request.form['inputCity']
	state = request.form['inputState']
	phone = request.form['inputPhone']
	passport_country = request.form['inputCountry']
	pass_num = request.form['inputPass_num']
	Pass_exp = request.form['inputPass_exp']

	#ERROR DOB retirns bad request
	
	#date = '0002-02-22'
	cursor = conn.cursor()
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute (query, (email))
	data=cursor.fetchone()
	error = None
	if(data):
		error = "This user already exists"
		#debug
		return render_template('signup_customer.html')
	else:
		ins = 'INSERT INTO customer(email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		

		cursor.execute(ins, (email, name, password, building, street, city, state, phone, pass_num, Pass_exp, passport_country, date))
		conn.commit()
		cursor.close()
		return render_template('signin.html')


	@app.route('/showLogin')
	def login_page():
		return render_template('login.html')

	@app.route('/SignIn')
	def SignIn():
		print('ENTER SignIn')
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

			return render_template('home_customer.html', user=email)

		else:
			error = 'Invalid login or username'
			return render_template('login.html', error=error)

@app.route('/profileCustomer', methods=['GET','POST'])
def profileCustomer():
	email = session['email']
	cursor = conn.cursor()
	query = 'SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.status FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE customer_email = %s'
	cursor.execute (query)
	data=cursor.fetchall()
	cursor.close()
	return render_template('home_customer.html', username=email, flights=data)

app.secret_key = 'some key that you will never guess'

if __name__ == "__main__":
    app.run()