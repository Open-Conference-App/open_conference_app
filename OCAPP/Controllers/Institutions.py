from OCAPP import app
from OCAPP.Models import Institution

@app.route('/institutions', methods=['POST'])
def create(id):
	inst = Institution.create({'name':request.form['name']})
