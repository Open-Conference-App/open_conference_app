from OCAPP.Models import Institution

@app.routes('/institutions', methods=['POST'])
def create(id):
	inst = Institution.create({'name':request.form['name']})
