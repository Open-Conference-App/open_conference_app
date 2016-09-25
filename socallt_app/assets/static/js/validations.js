function validate(page, valiArr){
	var valid = true
	//loop through validations for fields and apply classes if false
	for (var i=0; i<valiArr.length; i++){
		var name = '#' + valiArr[i]['fieldName'];
		valiArr[i]['valid'] = valiArr[i]['validation'](name) ? true : false;
		if(valiArr[i]['valid']){
			console.log(valiArr[i]['fieldName']);
			$(name).removeClass('is-danger');
		} else {
			$(name).addClass('is-danger'); 
			valid = false;
		}
	}
	return {'allValid' : valid, 'validations': valiArr}
}
//check the length as a validation
function checkLen(field, len, operator){
	if(operator == '>'){
		return $(field).val().length > len ? true : false;
	} else if(operator == '<'){
		return $(field).val().length < len ? true : false;
	} else if(operator == '='){
		return $(field).val().length == len ? true : false;
	} else {
		return 'Operator must be >, <, or =.'
	}
};

var page1_valids = [{
		'fieldName': 'first_name',
		'validation': (fieldname) => checkLen(fieldname, 1, '>'),
		'message': 'Last name must be present.'
	},
	{
		'fieldName': 'last_name',
		'validation': (fieldname) => checkLen(fieldname, 1, '>'),
		'message': 'Last name must be present.'
	},
	{
		'fieldName': 'email',
		'validation': function(fieldname){
			var email_patt = new RegExp($(fieldname).pattern);
			console.log(email_patt.test($(fieldname).val()))
			return email_patt.test($(fieldname).val()) && $(fieldname).val();
		},
		'message': 'Email is not formatted correctly.'
	},
	{
		'fieldName': 'password',
		'validation': (fieldname) => checkLen(fieldname, 8, '>'),
		'message': 'Passwords must be at least 8 characters.'
	},
	{
		'fieldName': 'confirm-password',
		'validation': (fieldname) => $(fieldname).val() == $('#password').val(),
		'message': 'Passwords do not match.'
	}
];

var page2_valids = [{
		'fieldName': 'street1',
		'validation': (fieldname) => checkLen(fieldname, 0, '>'),
		'message': 'Street1 must be provided.'
	},
	{
		'fieldName': 'street2',
		'validation': (fieldname) => true,
		'message': ''
	},
	{
		'fieldName': 'city',
		'validation': (fieldname) => checkLen(fieldname, 0, '>'),
		'message': 'City is required'
	},
	{
		'fieldName': 'state',
		'validation': (fieldname) => $(fieldname).val() ? true : false,
		'message': ''
	},
	{
		'fieldName': 'zip',
		'validation': (fieldname) => checkLen(fieldname, 5, '='),
		'message': 'Zip codes must be 5 digits.'
	},
	{
		'fieldName': 'instution',
		'validation': (fieldname) => $(fieldname).val(),
		'message': ''
	}];

var page3_valids = [{
		'fieldName': 'lunch',
		'validation': (fieldname) => checkLen(fieldname, 0, '>'),
		'message': 'A lunch option must must be provided.'
	},
	{
		'fieldName': 'gluten',
		'validation': (fieldname) => true,
		'message': ''
	},
	{
		'fieldName': 'payment',
		'validation': (fieldname) => checkLen(fieldname, 0, '>'),
		'message': 'Please select a payment type.'
	},
	{
		'fieldName': 'regType',
		'validation': (fieldname) => checkLen(fieldname, 0, '>'),
		'message': 'Registration type is required'
	},
	{
		'fieldName': 'regLen',
		'validation': (fieldname) => $(fieldname).val() ? true : false,
		'message': 'Registration days selection is required.'
	}];
