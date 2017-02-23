from OCAPP import app
import raven
from OCAPP import sentry
from OCAPP.config.sensitive import Sens
sens = Sens()
from flask import render_template, request, session, redirect, flash
from OCAPP.Models import Member, Conference, State, Institution
from OCAPP.Controllers import Mail
import datetime


@app.route('/members/<int:member_id>/change_password', methods=['POST'])
def change_password(member_id):
	member = Member.get_by_id(member_id)
	if not member:
		return redirect('/')
	pass_data = Member.change_password(member,request.form['password']) 
	if type(pass_data) is dict:
		for error in pass_data['errors']['password']:
			flash(error, 'passwordErr')
		return redirect('/members/' + str(member.id))
	flash('Password updated successfully.', 'passwordSuccess')
	return redirect('/members/' + str(member.id))

@app.route('/members/password_reset', methods=['POST'])
def generate_reset_password():
	if 'email' not in request.form:
		return redirect('/')
	member = Member.get_by_email(request.form['email'])
	if not member:
		flash('The email address you entered does not exist.', 'loginErr')
		return redirect('/')
	hash = Member.generate_reset_hash(member.id)
	if hash:
		data = {
                        'conf': Conference.get_next(),
			'hash': hash,
			'member': member
		}
		Mail.send({
			"subject": "SOCALLT Password Reset",
			"toAddy": member.email,
			"template": "password_reset.html",
               		"plain_message": "We received a request to reset your password.  If you did not request it, please email us as socalltofficers@gmail.com.  Otherwise, please click the following link to reset your password.",
			"data": {'data': data}	
		})
		return render_template('password_reset.html', data=data)
	return redirect('/')	

@app.route('/members/password_reset/<hash>', methods=['GET'])
def reset_password(hash):
	hash_record = Member.find_reset_hash(hash)
	if hash_record:
		diff = datetime.datetime.now() - hash_record.created_at
		if diff.days > 14:
			flash('The link you attempted to access is no longer valid.  Please request a new password reset.', 'loginErr')
			return redirect('/')  
		member = Member.get_by_id(hash_record.member_id)
		if not member:
			flash('The link you attempted to access is not associated with a member.', 'loginErr')
			return redirect('/')
		session['id'] = member.id
		session['email'] = member.email
		session['first_name'] = member.first_name
		session['admin'] = True if member.officer else False
		data = {
        	'conf': Conference.get_next(),
		'states': State.index(),
		'institutions': Institution.index()
		}
		return redirect('/members/' + str(member.id))
	flash('The link you attempted to access is not valid.', 'loginErr')
	return redirect('/')
	
@app.route('/members', methods=['GET'])
def show_members():
	if 'admin' not in session or not session['admin']:
		return redirect('/')
	members = Member.index()
	active = 0
	inactive = 0
	for mem in members:
		if mem.active:
			active += 1
		else:
			inactive += 1
	
	data = {
	'conf': Conference.get_next(),
	'states': State.index(),
	'institutions': Institution.index()
	}
	return render_template('/dashboard/admin/members.html', members=members, active=active, inactive=inactive, data=data)



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
		data = {
			'conf': Conference.get_next()
		}
		return render_template('dashboard/members/membership.html', member=member, data=data)
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
			data = {
			'conf': Conference.get_next(),
			'states': State.index(),
			'institutions': Institution.index()
			}
			return render_template('dashboard/members/membership.html', member=member, data=data)
		else:
			return redirect('/')

