from OCAPP.Models import Presentation, Conference, State, Institution
from OCAPP import app
from flask import render_template, session, request, redirect, flash 
import json


@app.route('/conferences/<int:conference_id>/proposals', methods=['GET'])
def proposal_form(conference_id):
	data = {
		'conf': Conference.get_next(),
		'states': State.index(),
		'institutions': Institution.index(),
		'presentation_types': Presentation.get_types()
	}
	return render_template('proposal_form.html', data=data)

@app.route('/conferences/<int:conference_id>/proposals/success', methods=['GET'])
def proposal_confirmation(conference_id):
	return render_template('proposal_confirmation.html')

@app.route('/presentations/proposals', methods=['GET'])
def show_proposals():
	if not session['admin']:
		return redirect('/')
	props = Presentation.get_current_proposals()
	for prop in props:
		if prop.nonmember_presenters:
			prop.decoded_nonmember_presenters = json.loads(prop.nonmember_presenters)
	data = {
	'conf': Conference.get_next(),
	'states': State.index(),
	'institutions': Institution.index(),
	'proposals': props
	}
	return render_template('dashboard/admin/proposals.html', data=data)

