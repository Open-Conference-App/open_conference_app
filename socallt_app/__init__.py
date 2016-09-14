from flask import Flask, session
from flask.ext.session import Session
from socallt_app.config import sensitive
import os
sens = sensitive.Sens()
app = Flask('socallt_app', static_folder=sens.root_path + '/assets/static', template_folder=sens.root_path + '/assets/templates')
app.secret_key = sens.secret_key
print app.template_folder
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
# Session(app)
import socallt_app.routes
app.config['SQLALCHEMY_DATABASE_URI'] = sens.db_path



