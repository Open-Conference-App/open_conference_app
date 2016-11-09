from OCAPP.config.sensitive import Sens
sens = Sens()
from OCAPP import app
from flask import Flask, session, url_for, request, render_template, redirect, flash
from OCAPP.Controllers import States, Addresses, Vendors, Institutions, Vendors, Conferences, Members, Presentations, Sessions

@app.route('/dash')
def dash():
	return redirect('/members/dashboard')






