from OCAPP import app
from OCAPP.config.sensitive import Sens
sens = Sens()
from flask import render_template, request, session, redirect
from OCAPP.Models import Member, Conference, State, Institution

@app.route('/members', methods=['GET'])
def show_members():
	if not session['admin']:
		return redirect('/')
	members = Member.index()
	return render_template('/dashboard/admin/members.html', members=members)



#create a new member(when users regsiter for the next conference)
@app.route('/members', methods=['POST'])
def create_memb():
	if not 'csrf_token' in session:
		return redirect('/conferences')
	#what's the route for admin dashboard??
	return redirect('/')


#creates new user in db (should be utilized if it is a new member only)
@app.route('/members/<int:member_id>', methods=['GET','PUT', 'DELETE'])
def handle_members(member_id):
	#show member info
	if request.method == 'GET':
		if 'id' not in session or session['id'] != member_id:
			return redirect('/')
		member = Member.get_by_id(member_id)
		return render_template('dashboard/members/membership.html', member=member)
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

@app.route('/members/<int:member_id>/conferences/<int:conference_id>', methods=['GET'])
def show(conference_id, member_id):
	if 'id' not in session or session['id'] != member_id:
		return redirect('/')
	member = Member.get_by_id(member_id)
	conference = Conference.get_by_id(conference_id)
	return render_template('member-conferences.html', member=member, conference=conference)

@app.route('/members/dashboard')
def load_dashboard():
	if 'id' in session:
		member = Member.get_by_id(session['id'])
		if member:
			return render_template('dashboard/dashboard.html', member=member)
		else:
			return redirect('/')

