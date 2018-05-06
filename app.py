from flask import Flask, Markup, render_template, request, session, url_for, redirect
import pymysql.cursors, datetime
app = Flask(__name__)
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='flight_booking',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
@app.route('/', methods=['GET', "POST"])
def main():
	return render_template('index.html')
@app.route('/main', methods=['GET', "POST"])
def show_index():
	return render_template('index.html')
@app.route('/showUsertype')
def ShowUsertype():

	return render_template('signup_usertype.html')
#author: Artem
@app.route('/Usertype_redirect', methods=['POST', 'GET'])
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
		error=None
		if(data):
			session['email'] = email
			session['logged_in'] = True
			cursor.close()

			return redirect(url_for('profileCustomer'))

		else:
			error = 'Invalid login or password'
			cursor.close()

			return render_template('login.html', error=error)
	elif type_user=='Booking Agent':
		query = 'SELECT * FROM booking_agent WHERE email = %s and password = %s'

		cursor.execute(query, (email, password))
		data = cursor.fetchone()
		error=None
		if(data):
			session['email'] = email
			session['logged_in'] = True
			cursor.close()

			return redirect(url_for('profileAgent'))
		else:
			error = 'Invalid login or password'
			cursor.close()
			return render_template('login.html', error=error)
	elif type_user=='Airline Staff':
		query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
		cursor.execute(query, (email, password))
		data = cursor.fetchone()
		error=None
		if(data):
			session['email'] = email
			session['logged_in'] = True

			cursor.close()

			return redirect(url_for('profileStaff'))
		else:
			error = 'Invalid login or password'
			cursor.close()
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
	email = request.form["1"]
	passw = request.form["2"]
	agentid = request.form["3"]

	cursor = conn.cursor()
	query = 'SELECT * FROM booking_agent WHERE email = %s'
	cursor.execute(query, (email))
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
		return redirect(url_for('showLogin'))
#author: Artem
@app.route('/signUpStaff', methods=['GET', 'POST'])
def signUpStaff():
	username = request.form['inputEmail']
	password = request.form['inputPassword']
	first_name = request.form['inputFirstName']
	last_name = request.form['inputLastName']
	dob = request.form['inputDOBd']
	airline = request.form['inputAirlineName']
	cursor = conn.cursor()
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute (query, (username))
	data=cursor.fetchone()
	error = None
	if(data):
		error = "This user already exists"
		#debug
		return render_template('signup_airlinestaff.html')
	else:
		ins = 'INSERT INTO airline_staff(username, password, first_name, last_name, date_of_birth, airline_name) VALUES(%s, %s, %s, %s, %s, %s)'
		

		cursor.execute(ins, (username, password, first_name, last_name, dob, airline))
		conn.commit()
		cursor.close()
		return render_template('login.html')
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

#author: artem
@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
	name = session['email']
	checkq = 'SELECT username from airline_staff where username = %s'
	cursor = conn.cursor()
	cursor.execute(checkq, (name))
	auth = cursor.fetchone()
	if(auth):
		name = request.form['airportA']
		city  =request.form['city']

		cursor = conn.cursor()
		query = 'SELECT airport_name from airport where airport_name = %s'
		cursor.execute(query, (name))
		data = cursor.fetchone()
		error = None
		if (data):
			error = 'This airport already exisits'
			return redirect(url_for('profileStaff'), error=error)
		else:
			ins = 'INSERT INTO `airport`(`airport_name`, `airport_city`) VALUES (%s, %s)'
			cursor.execute(ins, (name, city))
			conn.commit()
			cursor.close()
			return redirect(url_for('profileStaff'))
	else:
		error = 'you are not allowed to add airports'


#author: artem
@app.route('/add_plane', methods=['GET', 'POST'])
def add_plane():
	name = session['email']
	checkq = 'SELECT username from airline_staff where username = %s'
	cursor = conn.cursor()
	cursor.execute(checkq, (name))
	auth = cursor.fetchone()
	if(auth):
		airline = request.form['airline2']
		plane_id = request.form['airpl']
		seats = request.form['seat']
		cursor = conn.cursor()

		query = 'SELECT * from airplane where airplane_id = %s and airline_name = %s'
		cursor.execute(query, (plane_id, airline))
		data = cursor.fetchone()

		if (data):
			error = 'The plane with this ID already exists'
			return redirect(url_for('profileStaff'), error=error)
		else:
			ins = 'INSERT INTO `airplane`(`airline_name`, `airplane_id`, `seats`) VALUES (%s, %s, %s)'
			cursor.execute(ins, (airline, plane_id, seats))
			conn.commit()
			cursor.close()
			return redirect(url_for('profileStaff'))
	else: 
		error = 'you are not allowed to add planes'

#author: artem
@app.route('/change_status', methods=['GET', 'POST'])
def change_status():
	name = session['email']
	checkq = 'SELECT username from airline_staff where username = %s'
	cursor = conn.cursor()
	cursor.execute(checkq, (name))
	auth = cursor.fetchone()
	if(auth):
		line_name = request.form['airline3']
		plane_id = request.form['flight_id3']
		status = request.form['status']

		cursor = conn.cursor()

		query = 'update flight set status = %s where flight_num = %s and airline_name = %s'
		cursor.execute(query, (status, plane_id, line_name))
		conn.commit()
		cursor.close()
		return redirect(url_for('profileStaff'))
	else:
		error = 'you are not allowed to change the status of a flight'

#author: artem
@app.route('/add_flights', methods=['GET', 'POST'])
def add_flights():
	name = session['email']
	checkq = 'SELECT username from airline_staff where username = %s'
	cursor = conn.cursor()

	cursor.execute(checkq, (name))
	auth = cursor.fetchone()
	if(auth):
		flight_id = request.form['flight_id']
		airline = request.form['airline1']
		date_depart = request.form['date_dep']
		date_arr = request.form['date_arr']
		departure = request.form['departure']
		arrival = request.form['arrival']
		price = request.form['price']
		status = request.form['status']	
		plane_id = request.form['planeid']

		cursor = conn.cursor()
		query = 'SELECT * FROM flight WHERE flight_num = %s'
		cursor.execute (query, (flight_id))
		data = cursor.fetchone()


		if (data):
			error = 'The flight like this already exists.'
			return redirect(url_for('profileStaff'))
		else:
			ins = 'INSERT INTO `flight`(`airline_name`, `flight_num`, `departure_airport`, `departure_time`, `arrival_airport`, `arrival_time`, `price`, `status`, `airplane_id`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, %s)'
			 
			cursor.execute(ins, (airline, flight_id, departure, date_depart, arrival, date_arr, price, status, plane_id))	
			conn.commit()
			cursor.close()
			return redirect(url_for('profileStaff'))
	else:
		error = 'You are not allowed to add flights'
		
@app.route('/show_search_flights', methods=['GET', 'POST'])
def show_search_flight():
	return render_template('search_flights/\.html')

@app.route('/TEST', methods=['GET'])
def TEST():
	return ('TESTING')

@app.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
	
	date_depart = request.form['date_dep3']
	departure = request.form['departure3']
	arrival = request.form['arrival3']
	cursor = conn.cursor()

	

	query = 'select * from flight where DATE(departure_time)=%s and departure_airport = %s and arrival_airport=%s'

	

	cursor.execute(query, (date_depart, departure, arrival))
	results = cursor.fetchall()
	# return(str([date_depart, departure, arrival]))
	return render_template('search_flight.html', flights = results	)

@app.route('/search_passengers', methods=['GET', 'POST'])
def search_passengers():
	flight_id = request.form['flight_id3']
	airline = request.form['airline3']
	name = session['email']
	query = 'SELECT customer.email, customer.name, customer.phone_number, customer.date_of_birth, customer.state, customer.city, customer.street, customer.building_number from customer natural join ticket natural join flight where flight_num = %s and airline_name = %s'
	cursor = conn.cursor()
	cursor.execute(query, (flight_id, airline))
	passengers = cursor.fetchall()
	return render_template('search_passengers.html', passengers = passengers, curr_flight = flight_id, curr_line = airline, username = name)






#author: artem
@app.route('/customers_flights', methods=['GET', 'POST'])
def customers_flights():
	username = session['email']
	email = request.form['email4']
	cursor = conn.cursor()
	queryLine  ='select airline_name from airline_staff where username = %s'
	cursor.execute(queryLine, (username))
	cur_line = cursor.fetchone()['airline_name']


	query = 'SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.status from customer natural join ticket natural join flight natural join purchases where customer.email = %s'
	cursor.execute(query, (email))
	flight = cursor.fetchall()
	return render_template('search_cus_flight.html', username = username,  flights = flight, customer_name = email, curr_line = cur_line)

def curr_line(email):
	q = 'select airline_name from airline_staff where username = %s'
	cursor = conn.cursor()
	cursor.execute(q, (email))

	ln = cursor.fetchone()
	return ln['airline_name']
#author: Artem
@app.route('/profileStaff', methods=['GET', 'POST'])
def profileStaff():
	email = session['email']
	checkq = 'SELECT username from airline_staff where username = %s'
	cursor = conn.cursor()
	# if session['logged_in'] == True:
	# 	return('hello')
	# else:
	# 	return('bye')
	cursor.execute(checkq, (email))
	auth = cursor.fetchone()
	if(auth) and session['logged_in'] == True:
		queryFlights = 'SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.status FROM flight natural join airline_staff where airline_staff.username = %s and flight.departure_time < date(now() + interval 30 day) and flight.departure_time > date(now()) '
		cursor.execute(queryFlights, (email))
		flights = cursor.fetchall()


		queryAgentsm = 'SELECT booking_agent_id, count(ticket_id) as sold from booking_agent natural join purchases natural join ticket where purchases.purchase_date > date(now() - interval 1 month) and ticket.airline_name = (select airline_name from airline_staff where username= %s)  group by booking_agent_id  order by count(ticket_id) desc limit 5'
		cursor.execute(queryAgentsm, (email))
		agents_purchase_month = cursor.fetchall()

		queryAgentsy = 'SELECT booking_agent_id, count(ticket_id) as sold from booking_agent natural join purchases natural join ticket where purchases.purchase_date > date(now() - interval 1 year) and ticket.airline_name = (select airline_name from airline_staff where username= %s)  group by booking_agent_id  order by count(ticket_id) desc limit 5'
		cursor.execute(queryAgentsy, (email))
		agents_purchase_year = cursor.fetchall()

		queryComission = "SELECT booking_agent_id, sum(price) as sold from booking_agent natural join purchases natural join ticket natural join flight where purchases.purchase_date > date(now() - interval 1 year) and ticket.airline_name = (select airline_name from airline_staff where username= %s)  group by booking_agent_id  order by count(ticket_id) desc limit 5"
		cursor.execute(queryComission, (email))
		agents_comission = cursor.fetchall()

		queryFreqCust = 'select customer.email, customer.name, customer.phone_number, customer.date_of_birth, customer.state, customer.city, customer.street, customer.building_number from customer inner join purchases on purchases.customer_email= customer.email natural join ticket where ticket.airline_name = (select airline_name from airline_staff where username = %s) and purchase_date > date(now()-interval 1 year) group by customer.email ORDER by count(ticket_id) desc limit 10'
		cursor.execute(queryFreqCust, (email))
		customers = cursor.fetchall()

		queryDest3m = 'SELECT * from airport inner join (select arrival_airport from flight natural join ticket where flight.departure_time> date(now() - interval 3 month) and flight.airline_name = (select airline_name from airline_staff where username = %s)) as arr'
		cursor.execute(queryDest3m, (email))
		dest3M = cursor.fetchall()
		queryDestY = 'SELECT * from airport inner join (select arrival_airport from flight natural join ticket where flight.departure_time> date(now() - interval 1 year) and flight.airline_name = (select airline_name from airline_staff where username = %s) order by count(flight.flight_num) desc) as arr'
		cursor.execute(queryDestY, (email))
		dest1Y = cursor.fetchall()




		qAirports = 'SELECT * from airport'
		cursor.execute(qAirports)
		all_airports = cursor.fetchall()

		qStatus = 'select distinct(status) from flight'
		cursor.execute(qStatus)
		statuses = cursor.fetchall()


		qPlanes = 'select airplane_id from airplane where airplane.airline_name = (select airline_name from airline_staff where username = %s)'
		cursor.execute(qPlanes, (email))
		planes = cursor.fetchall()

		qAllPlanes = 'SELECT * from airplane where airplane.airline_name = (select airline_name from airline_staff where username = %s)'
		cursor.execute(qAllPlanes, (email))
		allplanes = cursor.fetchall()

		qAllFlights = 'SELECT flight_num from flight where airline_name = (select airline_name from airline_staff where username = %s)'
		cursor.execute(qAllFlights, (email))
		allFlights = cursor.fetchall()

		qLines = 'select airline_name from airline_staff where username = %s'
		cursor.execute(qLines,(email))
		airlines = cursor.fetchall()

		qcurr_line = 'select airline_name from airline_staff where username = %s'
		cursor.execute(qcurr_line,(email))
		curr_line = cursor.fetchone()['airline_name']

		

		colors = ["#F7464A", "#46BFBD"]
		pie_labelsM = []
		pie_valuesM = []
		pie_labelsY = []
		pie_valuesY = []


		pie_labelsM = ['Direct', 'Agent']
		pie_labelsY = ['Direct', 'Agent']
		

		

		queryRevMdirect = 'select sum(price) from flight natural join ticket natural join purchases where booking_agent_id is Null and departure_time > date(now() - interval 1 month ) and flight.airline_name = (select airline_name from airline_staff where username = %s)'

		cursor.execute(queryRevMdirect, (email))
		revMdirect = cursor.fetchall()

		for row in revMdirect:
			for col in row:
				pie_valuesM.append(int(row[col]))


		queryRevMagent = 'select sum(price) from flight natural join ticket natural join purchases where booking_agent_id is not Null and departure_time > date(now() - interval 1 month) and flight.airline_name = (select airline_name from airline_staff where username = %s)'
		cursor.execute(queryRevMagent, (email))
		revMagent = cursor.fetchall()

		for row in revMagent:
			for col in row:
				pie_valuesM.append(int(row[col]))

		queryRevYdirect = 'select sum(price) from flight natural join ticket natural join purchases where booking_agent_id is Null and departure_time > date(now() - interval 1 year ) and flight.airline_name = (select airline_name from airline_staff where username = %s)'

		cursor.execute(queryRevYdirect, (email))
		revYdirect = cursor.fetchall()

		queryRevYagent = 'select sum(price) from flight natural join ticket natural join purchases where booking_agent_id is not Null and departure_time > date(now() - interval 1 year) and flight.airline_name = (select airline_name from airline_staff where username = %s)'
		cursor.execute(queryRevYagent, (email))
		revYagent = cursor.fetchall()

		for row in revYdirect:
			for col in row:
				pie_valuesY.append(int(row[col]))

		for row in revYagent:
			for col in row:
				pie_valuesY.append(int(row[col]))


		return render_template('home_staff.html', username = email, curr_line  =curr_line, allFlights = allFlights, airlines = airlines, airports = all_airports, allplanes =allplanes, stats = statuses, planes = planes, flights = flights, agents_month = agents_purchase_month, agents_year = agents_purchase_year, comission = agents_comission, customers = customers, dest3M = dest3M, dest1Y = dest1Y, for_month = zip(pie_valuesM, pie_labelsM, colors), for_year = zip(pie_valuesY, pie_labelsY, colors), max = 10000)
		# return render_template('home_staff.html', set=zip(values, labels, colors), username = email, curr_line  =curr_line, allFlights = allFlights, airlines = airlines, airports = all_airports, allplanes =allplanes, stats = statuses, planes = planes, flights = flights, agents_month = agents_purchase_month, agents_year = agents_purchase_year, comission = agents_comission, customers = customers, dest3m = dest3M, dest1Y = dest1Y, for_month = zip(pie_valuesM, pie_labelsM, colors), for_year = zip(pie_valuesY, pie_labelsY, colors), max = 10000, labelsBar = labelsBar, valuesBar = valuesBar, stepsBar = stepsBar ,maxspendingBar = maxbuyBar)
	else:
		error = 'you are not logged in as staff'
		return redirect(url_for('show_index'))

#author: artem
@app.route('/profileStaffDates', methods=['GET', 'POST'])
def profileStaffDates():
	
	email = session['email']
	fromm = request.form['inputFrom']
	# print(fromm)	
	ln = curr_line(email)	
	to = request.form['inputTo']
	cursor = conn.cursor()



	if fromm == '' and to != '':
		query = 'SELECT count(ticket_id) as sold, extract(year from departure_time) as yr, monthname(departure_time) as mth, extract(YEAR_MONTH from departure_time) as dt from flight natural join ticket where departure_time <=%s  group by dt'


		# where yr <= extract(year from %s) and mth <= extract(month from %s)'
		cursor.execute(query, (to))
		data = cursor.fetchall()
		labels = []
		values = []

		
		for i in data:
			labels.append(str(i['mth']) + ' '+ str(i['yr']))
			values.append(int(i['sold']))

		steps = len(values)
		if steps == 0:
			maxbuy = 0
		else:
			maxbuy = int(max(values))
		
		return render_template('tickets_bar.html', username = email, curr_line = ln,labels = labels, values = values, steps = steps ,maxspending = maxbuy)


		


	elif to == '' and fromm!='':
		query = 'SELECT count(ticket_id) as sold, extract(year from departure_time) as yr, monthname(departure_time) as mth, extract(YEAR_MONTH from departure_time) as dt from flight natural join ticket where departure_time >=%s  group by dt'


		# where yr <= extract(year from %s) and mth <= extract(month from %s)'
		cursor.execute(query, (fromm))
		data = cursor.fetchall()
		labels = []
		values = []

		
		for i in data:
			labels.append(str(i['mth']) + ' '+ str(i['yr']))
			values.append(int(i['sold']))
		steps = len(values)
		if steps == 0:
			maxbuy = 0
		else:
			maxbuy = int(max(values))


		return render_template('tickets_bar.html', username = email, curr_line = ln,labels = labels, values = values, steps = steps ,maxspending = maxbuy)
	elif fromm!='' and to !='':
		query = 'SELECT count(ticket_id) as sold, extract(year from departure_time) as yr, monthname(departure_time) as mth, extract(YEAR_MONTH from departure_time) as dt from flight natural join ticket where departure_time between %s and  %s group by dt'


		# where yr <= extract(year from %s) and mth <= extract(month from %s)'
		cursor.execute(query, (fromm, to))
		data = cursor.fetchall()
		labels = []
		values = []

		
		for i in data:
			labels.append(str(i['mth']) + ' '+ str(i['yr']))
			values.append(int(i['sold']))
		steps = len(values)

		if steps == 0:
			maxbuy = 0
		else:
			maxbuy = int(max(values))


		
		return render_template('tickets_bar.html', username = email, curr_line = ln,labels = labels, values = values, steps = steps ,maxspending = maxbuy)
	else:
		#ALL FLIGHTS		
		query = 'select count(ticket_id) as sold, extract(year from departure_time) as yr, monthname(departure_time) as mth, extract(YEAR_MONTH from departure_time) as dt from flight natural join ticket group by dt'
		cursor.execute(query)
		data = cursor.fetchall()
		ii = ''
		labels = []
		values = []

		
		for i in data:
			labels.append(str(i['mth']) + ' '+ str(i['yr']))
			values.append(int(i['sold']))
		steps = len(values)

		if steps == 0:
			maxbuy = 0
		else:
			maxbuy = int(max(values))


		
		return render_template('tickets_bar.html', username = email, curr_line = ln,labels = labels, values = values, steps = steps ,maxspending = maxbuy)




#author: Amin
@app.route('/profileCustomer', methods=['GET','POST'])
def profileCustomer():
	email = session['email']
	cursor = conn.cursor()
	if session['logged_in'] == True:
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
	else:
		return redirect(url_for('show_index'))

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
	if session['logged_in'] == True:
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
	else:
		return redirect(url_for('show_index'))

#author: Amin
@app.route('/profileAgentDates', methods=['GET','POST'])
def profileAgentDates():
	email = session['email']
	commissionFrom = request.form['inputFrom']
	commissionTo = request.form['inputTo']
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
	cursor.execute (query2, (email, commissionFrom, commissionTo))
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
@app.route('/profileAgent2', methods=['GET','POST'])
def profileAgent2():
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
	fromTwelveYear = str(int(nowYear)-1)
	# print(fromTwelveYear)
	fromTwelve = fromTwelveYear + '-' + nowMonth + '-' + nowDay
	cursor = conn.cursor()
	query4 = 'SELECT * FROM (SELECT customer_email, SUM(price/10) as commission FROM purchases NATURAL JOIN booking_agent NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent.email = %s AND purchase_date BETWEEN %s AND %s GROUP BY customer_email ORDER BY commission DESC) as t1 LIMIT 5'
	cursor.execute (query4, (email, fromTwelve, to))
	data4=cursor.fetchall()
	labels = []
	values = []
	for entry in data4:
		for e in entry:
			if e == 'customer_email':
				labels.append(entry[e])
			elif e == 'commission':
				values.append(entry[e])
	# print(labels, values)
	try:
		maxCommission = max(values)
	except ValueError:
		maxCommission = 10

	cursor.close()
	return render_template('home_agent2.html', username = email, labels = labels , values = values, maxCommission = maxCommission)

#author: Amin
@app.route('/flightStatus', methods=['GET','POST'])
def flightStatus():
	airlineName = request.form['inputAirlineName']
	flightNumber = request.form['inputFlightNumber']
	departureDate = request.form['dat']
	likeDepartureDtae = '%' + departureDate + '%'
	cursor = conn.cursor()
	query = 'SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.status FROM flight WHERE airline_name = %s AND flight_num = %s AND departure_time LIKE %s'
	cursor.execute (query, (airlineName, flightNumber, likeDepartureDtae))
	data=cursor.fetchall()
	if (data):
		return render_template('index.html', status = data)
	else:
		error = 'Invalid flight details'
		return render_template('index.html', error=error)

#author: Atem
@app.route('/buyFlight', methods=['GET','POST'])
def buyFlight():
	buyAirlineName = request.form['buyAirlineName']

	


	buyFlightNumber = request.form['buyFlightNumber']

	buyEmail = request.form['buyEmail']

	buyPass = request.form['buyPass']

	buyAgent = request.form['buyAgent']

	buyCust = request.form['buyCust']
	cursor = conn.cursor()
	qticketID = 'SELECT max(ticket_id) as m from ticket'
	cursor.execute(qticketID)
	ID = cursor.fetchone()['m'] +1
	qF = "SELECT * from flight where airline_name =%s and flight_num =%s"
	cursor.execute(qF, (buyAirlineName, buyFlightNumber))
	fdata = cursor.fetchone()

	if (fdata):
		if buyAgent != '':
			q = 'SELECT * from booking_agent where email =%s and password=%s and booking_agent_id=%s'
			cursor.execute(q,(buyEmail, buyPass, buyAgent))
			data = cursor.fetchone()
			#check if agent exists -> check if flight exists
			if (data):
				
				qtickA = 'INSERT INTO `ticket`(`ticket_id`, `airline_name`, `flight_num`) VALUES (%s, %s, %s)'
				cursor.execute(qtickA, (ID, buyAirlineName, buyFlightNumber))

				qpurchA = 'INSERT INTO `purchases`(`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES (%s, %s, %s, date(now()))'
				cursor.execute(qpurchA, (ID, buyCust, buyAgent))

				session['email'] = buyEmail
				session['logged_in'] = True
				conn.commit()
				cursor.close()
				return (redirect(url_for('profileAgent')))


		else:
			q = 'SELECT * from customer where email =%s and password=%s '
			cursor.execute(q,(buyEmail, buyPass))
			data = cursor.fetchone()
			#check if customer exists -> check if flight exists
			if (data):
				
				qtickC = 'INSERT INTO `ticket`(`ticket_id`, `airline_name`, `flight_num`) VALUES (%s, %s, %s)'
				cursor.execute(qtickC, (ID, buyAirlineName, buyFlightNumber))

				qpurchC = 'INSERT INTO `purchases`(`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES (%s, %s, NULL, date(now()))'
				cursor.execute(qpurchC, (ID, buyEmail))
				session['email'] = buyEmail
				session['logged_in'] = True

				conn.commit()
				cursor.close()
				return (redirect(url_for('profileCustomer')))
		conn.commit()
		cursor.close()


			# qbuy = 

	return (redirect(url_for('show_index')))

#author: Amin
@app.route('/logout')
def logout():
	email = session['email']
	session['logged_in'] = False
	session.pop(email, None)
	return redirect('/showLogin')

app.secret_key = 'some key that you will never guess'

if __name__ == "__main__":
    app.run(debug=True)