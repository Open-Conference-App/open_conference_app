from OCAPP import app
from OCAPP.Models import Address
from OCAPP.config.sensitive import Sens
import json

@app.route('/addresses', methods=['POST'])
def create_address():
	return json.dumps(Address.create(request.form.copy()))

@app.route('/conferences/<int:address_id>', methods=['GET','DELETE','PUT'])
def handle_address(address_id):
	#show next conference registration page, even if using a past conference idnumber or a non-int type
	if request.method == 'GET':
		new_address = Address.get_next()

		#if the parameter in uri is not a number or not the latest id, go to the latest
		if conference_id != new_conference.id:
			return redirect('/conferences/', new_conference.id)
		else:
			return render_template('index.html', conference={'id':address_id, 'year': new_address.id})

	#delete a conference(to be done through admin dashboard only as an ajax call)
	if request.method == 'DELETE':
		return json.dumps({'result': Address.destroy(conference_id)})

	#update conference information(to be done through admin dashboard only as an ajax call)
	if request.method =='PUT':
		address = Address.get_by_id(conference_id)
		changed_address = Address.update(address, request.form['address'])
		return json.dumps({'conference':changed_conference})