from OCAPP import app
from OCAPP.Models import Institution

@app.route('/institutions', methods=['POST'])
def create(id):
	inst = Institution.create({'name':request.form['name']})


@app.route("/create-inst", methods=["POST"])
def create_inst():
	print request.form.copy()
	
def create_inst2(name):
	inst = Institution.create({'name':name})
	