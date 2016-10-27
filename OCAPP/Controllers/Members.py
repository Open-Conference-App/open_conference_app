from OCAPP import app
from flask import render_template
from OCAPP.Models import Member, Conference, State, Institution
#create a new member(when users regsiter for the next conference)
@app.route('/')
def load_forms():
	data = {
		'conference': Conference.get_next(),
		'states': State.index(),
		'institutions': Institution.index()
	}
	
	return render_template('index.html', data=data)

@app.route('/members', methods=['POST'])	
def create_memb():
	if not 'csrf_token' in session:
		return redirect('/conferences')
	#what's the route for adming dashboard??
	return redirect('/')




#creates new user in db (should be utilized if it is a new member only)
@app.route('/members/<member_id>', methods=['GET','PUT', 'DELETE'])
def handle_members(member_id):
	#show member info
	if request.method == 'GET':
		if not isinstance(member_id, (int, long)):
			member = Members.get_by_id(member_id)
		return render_template('dashboard-test.html', name=member.first_name)
	#delete a conference(to be done through admin dashboard only)
	if request.method == 'DELETE':
		return redirect('/')

	#update conference information(to be done through admin dashboard only)
	if request.method =='PUT':
		form_data = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'email':request.form['email'],
			'password': request.form['password'],
			'confirm_password': request.form['confirm_password'],
			'street1': request.form['street1'],
			'street2': request.form['street2'],
			'city': request.form['city'],
			'state': request.form['state'],
			'zip': request.form['zip']
		}

		result = Members.create(form_data)
	if result:
		form_data = {}
		if 'inst-name' in request.form:
			form_data['inst-name'] = request.form['inst-name']
			form_data['inst-state'] = request.form['inst-state']
			inst = Institutions.create(form_data)
	if result:
		return redirect('/dashboard')
	else:
		return redirect('/')

@app.route('/members/dashboard')
def load_dashboard():
	if '_id' in session:
		session['csrf_token'] = sens.gen_csrf_token()
		return render_template('dashboard.html')
	else:
		return redirect('/')
