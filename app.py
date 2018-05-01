from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors, datetime
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
#author: Artem
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

#author: Artem
@app.route('/showLogin', methods=['GET', "POST"])
def showLogin():
	return render_template('login.html')
#author: Artem
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
			return redirect(url_for('profileAgent'))
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
			return redirect(url_for('profileStaff'))
		else:
			error = 'Invalid login or password'
			return render_template('login.html', error=error)



#author: Artem
@app.route('/showSignUpCustomer')
def showSignUpCustomer():

	return render_template('signup_customer.html')
#author: Artem
@app.route('/ShowSignUpStaff')
def ShowSignUpStaff():
	return render_template('signup_staff.html')
#author: Artem
@app.route('/ShowSignUpAgent')
def ShowSignUpAgent():
	return render_template('signup_agent.html')
#author: Artem
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
#author: Artem
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
#author: Artem
@app.route('/signUpCustomer', methods=['GET','POST'])
def signUpCustomer():
	email = request.form['inputEmail']

	password = request.form['inputPassword']

	name = request.form['inputName']

	date = request.form['dob']
	#ERROR DOB retirns bad request
	

	#ERROR DOB retirns bad request
	
	building = request.form['building']
	street = request.form['inputStreet']
	city = request.form['inputCity']
	state = request.form['inputState']
	phone = request.form['inputPhone']
	passport_country = request.form['inputCountry']
	pass_num = request.form['inputPass_num']
	Pass_exp = request.form['inputPass_exp']

	
	#date = '0002-02-22'
	cursor = conn.cursor()
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute (query, (email))
	data=cursor.fetchone()
	error = None
	if(data):
		error = "This user already exists"
		# EDIT ADD ERROR MESSAGE
		return render_template('signup_customer.html')
	else:
		ins = 'INSERT INTO customer(email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		

		cursor.execute(ins, (email, name, password, building, street, city, state, phone, pass_num, Pass_exp, passport_country, date))
		conn.commit()
		cursor.close()
		return render_template('index.html')


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
#author: Amin
@app.route('/profileCustomer', methods=['GET','POST'])
def profileCustomer():
	email = session['email']
	cursor = conn.cursor()
	query = 'SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.status FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE customer_email = %s'
	cursor.execute (query, (email))
	data=cursor.fetchall()
	
	# months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'Novermber', 'December']
	# labels = ["January","February","March","April","May","June"]
	# values = [10,9,8,7,6,4]
	query2 = 'SELECT extract(YEAR_MONTH FROM purchase_date) AS date, SUM(price) as monthly_spending FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE customer_email = %s GROUP BY date'
	cursor.execute (query2, (email))
	data2=cursor.fetchall()
	months = []
	years = []
	spending = []
	for entry in data2:
		for e in entry:
			if e == 'date':
				if str(entry[e])[-2] != '0':
					month = str(entry[e])[-2:]
					# print(month)
					months.append(month)
				else:
					month = str(entry[e])[-1]
					months.append(month)
				year = str(entry[e])[:4]
				years.append(year)
			elif e == 'monthly_spending':
				spending.append(int(entry[e]))
	
	now = datetime.datetime.now()
	# print(now)
	# print (now.year, now.month, now.day, now.hour, now.minute, now.second)

	allMonths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	lastSixMonths = []
	lastSixMonthsYears = []
	labels = []
	values =[]
	m = now.month
	y = now.year
	# (print(m))
	lastSixMonths.append(str(m))
	ind = allMonths.index(m)
	lastSixMonthsYears.append(str(y))

	for m in range(5):
		ind-=1
		lastSixMonths.append(str(allMonths[ind]))
		if ind >= 0:
			lastSixMonthsYears.append(str(y))
		else:
			lastSixMonthsYears.append(str(y-1))

	for j in range (len(lastSixMonths)-1, -1, -1):
		match = False
		labels.append(lastSixMonths[j] + '-' + lastSixMonthsYears[j])
		for k in range (len(months)-1, -1, -1):
			if lastSixMonths[j] == months[k] and lastSixMonthsYears[j] == years[k]:
				values.append(spending[k])
				match = True
		if match == False:
			values.append(0)

	maxSpending = max(values)
	# print(lastSixMonths)
	# print(lastSixMonthsYears)
	# print(months)
	# print(years)
	# print(labels)
	# print(values)
	
	cursor.close()
	return render_template('home_customer.html', username=email, flights=data, labels=labels, values=values, maxSpending = maxSpending)
#author: Amin
@app.route('/profileCustomerDates', methods=['GET','POST'])
def profileCustomerDates():
	email = session['email']
	fromm = request.form['inputFrom']
	# print(fromm)
	to = request.form['inputTo']
	# print(to)
	cursor = conn.cursor()
	query = 'SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.status FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE customer_email = %s'
	cursor.execute (query, (email))
	data=cursor.fetchall()
	
	query2 = 'SELECT extract(YEAR_MONTH FROM purchase_date) AS date, SUM(price) as monthly_spending FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE customer_email = %s AND purchase_date BETWEEN %s AND %s GROUP BY date'
	cursor.execute (query2, (email, fromm, to))
	data2=cursor.fetchall()
	months = []
	years = []
	spending = []
	# print(data2)
	for entry in data2:
		for e in entry:
			if e == 'date':
				if str(entry[e])[-2] != '0':
					month = str(entry[e])[-2:]
					print(month)
					months.append(month)
				else:
					month = str(entry[e])[-1]
					months.append(month)
				year = str(entry[e])[:4]
				years.append(year)
			elif e == 'monthly_spending':
				spending.append(int(entry[e]))
	# print(months, years, spending)
	
	labels = []
	for i in range (len(months)):
		labels.append(months[i] + '-' + years[i])
	values = spending

	try:
		maxSpending = max(values)
	except ValueError:
		maxSpending = 1000
	
	cursor.close()
	return render_template('home_customer.html', username=email, flights=data, labels=labels, values=values, maxSpending = maxSpending)
#author: Amin
@app.route('/profileAgent', methods=['GET','POST'])
def profileAgent():
	email = session['email']
	now = datetime.datetime.now()
	nowDay = str(now.day)
	if len(nowDay) == 1:
		nowDay = '0' + nowDay
	nowMonth = str(now.month)
	if len(nowMonth) == 1:
		nowMonth = '0' + nowMonth
	nowYear = str(now.year)
	to = nowYear + '-' + nowMonth + '-' + nowDay
	if nowMonth == '01':
		fromMonth = '12'
		fromYear = str(int(nowYear)-1)
	else:
		fromMonth = str(int(nowMonth)-1)
		fromYear = nowYear
	if len(fromMonth) == 1:
		fromMonth = '0' + fromMonth
	fromm = fromYear + '-' + fromMonth + '-' + nowDay
	# print(fromm)
	# print(type(fromm))
	# print(to)
	# print(type(to))
	cursor = conn.cursor()
	query = 'SELECT customer.email, customer.name, customer.password, flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.status FROM flight NATURAL JOIN ticket NATURAL JOIN purchases, customer, booking_agent WHERE customer.email = purchases.customer_email AND purchases.booking_agent_id = booking_agent.booking_agent_id AND booking_agent.email = %s'
	cursor.execute (query, (email))
	data=cursor.fetchall()

	query2 = 'SELECT tickets_sold, total_commission, total_commission/tickets_sold AS average_commission FROM (SELECT COUNT(ticket_id) AS tickets_sold, SUM(price)/10 AS total_commission FROM flight NATURAL JOIN ticket NATURAL JOIN purchases NATURAL JOIN booking_agent WHERE booking_agent.email = %s AND purchase_date BETWEEN %s AND %s) AS t1'
	cursor.execute (query2, (email, fromm, to))
	data2=cursor.fetchall()

	labels = []
	values = []
	months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
	sixMonthIndex = months.index(nowMonth)-6
	fromSixMonth = months[sixMonthIndex]
	if sixMonthIndex < 0:
		fromSixYear = str(int(nowYear)-1)
	else:
		fromSixYear = nowYear
	if len(fromSixMonth) == 1:
		fromMonth = '0' + fromMonth
	fromSix = fromSixYear + '-' + fromSixMonth + '-' + nowDay
	query3 = 'SELECT customer_email, num_tickets FROM (SELECT customer_email, COUNT(ticket_id) AS num_tickets FROM purchases NATURAL JOIN booking_agent WHERE booking_agent.email = %s AND purchase_date BETWEEN %s AND %s GROUP BY customer_email ORDER BY num_tickets DESC) as t1 LIMIT 5'
	cursor.execute (query3, (email, fromSix, to))
	data3=cursor.fetchall()
	for entry in data3:
		for e in entry:
			if e == 'customer_email':
				labels.append(entry[e])
			elif e == 'num_tickets':
				values.append(entry[e])
	# print(labels, values)
	try:
		maxTickets = max(values)
	except ValueError:
		maxTickets = 10

	cursor.close()
	return render_template('home_agent.html', username = email, flights = data, commission = data2, labels = labels , values = values, maxTickets = maxTickets)
#author: Amin
# @app.route('/profileAgentDates', methods=['GET','POST'])
# def profileAgentDates():
#author: Amin
@app.route('/logout')
def logout():
	email = session['email']
	session.pop(email, None)
	return redirect('/showLogin')

app.secret_key = 'some key that you will never guess'

if __name__ == "__main__":
    app.run(debug=True)