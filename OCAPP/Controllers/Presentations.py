from OCAPP.Models import Presentation, Conference, State, Institution
from OCAPP import app
from flask import render_template, session, request, redirect, flash 


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