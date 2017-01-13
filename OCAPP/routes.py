from OCAPP.config.sensitive import Sens
sens = Sens()
from OCAPP import app
from flask import Flask, session, url_for, request, render_template, redirect, flash
from OCAPP.Controllers import States, Addresses, Vendors, Institutions, Vendors, Conferences, Members, Presentations, Sessions
from OCAPP.Models import Conference, State, Institution


@app.route('/dash')
def dash():
	member = {'id': 1}
	data = {
			'conf': Conference.get_next(),
			'states': State.index(),
			'institutions': Institution.index()
			}
	return render_template('credit_card.html', member=member, data=data)






