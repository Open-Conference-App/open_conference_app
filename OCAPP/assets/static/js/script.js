$(document).ready(function(){
	validations = {
		'page1_valids': [{
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
					// console.log(email_patt.test($(fieldname).val()))
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
		],
		'page2_valids': [{
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
				'validation': (fieldname) => $(fieldname+' option:selected').val() != '' ? true : false,
				'message': ''
			},
			{
				'fieldName': 'zip',
				'validation': (fieldname) => checkLen(fieldname, 5, '='),
				'message': 'Zip codes must be 5 digits.'
			},
			{
				'fieldName': 'instution',
				'validation': function(fieldname){
					if($('#institution').val() < 0){
						return false;
					} else if($('#inst-name').val() == ''){
						return false;
					}
					return true;
				},
				'message': ''
			}],

	'page3_valids': [
		

		{
			'fieldName': 'lunch',
			'validation': function(fieldname) {
				value = $(fieldname+' option:selected').val()
				console.log(value)
				if(value == 'Regular' || value == 'Vegan' || value == "Vegeterian" || value == "NoLunch") {
					return true
				}
				return false
			},
			'message': 'A lunch option must must be provided.'
		},
		{
			'fieldName': 'gluten',
			'validation': (fieldname) => true,
			'message': ''
		},
		{
			'fieldName': 'pay',
			'validation': function(fieldname) {
				value = $(fieldname+' option:selected').val()
				if(value == 'credit_debit' || value == 'check_PO') {
					return true
				}
				return false
			},			
			'message': 'Please select a payment type.'
		},
		{
			'fieldName': 'regis-type',
			'validation': function(fieldname) {
				value = $(fieldname+' option:selected').val()
				if(value == 'Professional' || value == 'Student' || value == 'Vendor') {
					return true
				}
				return false
			},
			'message': 'Registration type is required'
		},
		{
			'fieldName': 'regis-len',
			'validation': function(fieldname) {
				value = $(fieldname+' option:selected').val()
				if(value == 'friday' || value == 'saturday' || value == 'weekend') {
					return true
				}
				return false
			},			
			'message': 'Registration days selection is required.'
		}]
	}

	//toggle view of login & registration forms	
	var user;
	$('button').click(function(){
		if($(this).attr('data-id')){
			var id = $(this).attr('data-id');
			var other = id == 'login' ? 'register' : 'login';
			$('#show-' + id).hide();
			$('#' + other + '-form').hide();
			$('#' + id + '-form').slideToggle();
			$('#show-' + other).slideToggle();
		}
	});

	//display inputs for a new institution if 'other' is selected
	$('#institution').change(function(){
		console.log('test')
		if(document.getElementById('other').selected){
			$('#inst-info').slideToggle();
		} else {
			$('#inst-info').slideUp();
		}
	});


		//populate price in regis_len
	$('#regis-type').change(function(){
		console.log($())
		var val = $('#regis-type').children(':selected').val()
		$.ajax({
			method: 'GET',
			url: '/conferences/' + confId + '/prices',
			success: function(data){
				var val = $('#regis-type').children(':selected').val()
				val = val == 'Student' ? 'stud_cost' : val == 'Profession' ? 'prof_cost' : 'vend_cost';
				data = JSON.parse(data);
				var price = data[val];
				var halfPrice = price/2;
				$('#regis-len').children()[1].innerHTML = 'Friday Only ($' + halfPrice.toFixed(2) + ')';
				$('#regis-len').children()[2].innerHTML = 'Saturday Only ($' + halfPrice.toFixed(2) + ')';
				$('#regis-len').children()[3].innerHTML = 'Entire Conference ($' + price.toFixed(2) + ')';
			}
		})
	});



	var member = {};
	$(document).on('click', '.continue', function(){
		//run validations based on page div id and validations
		var pageId = $(this).parent().parent().attr('id');
		var validArr = pageId + '_valids';
		var validObj = validate(pageId, validations[validArr]);
		//send member object to server if all validations were successful
		if(validObj.allValid) {
			for(var i = 0; i < validObj.validations.length; i++){
				member[validObj.validations[i]['fieldName']] = $('#'+validObj.validations[i]['fieldName']).val();
			}
			var nextPage = pageId == 'page1' ? 'page2' : pageId == 'page2' ? 'page3' : false;
			if(!nextPage){
				$('#register-form form').submit()
			} else {
				$('#'+pageId).hide();
				$('#'+nextPage).fadeToggle();
			}
		}
		return false;
	});

	$(document).on('click', '.previous', function(){
		var pageId = $(this).parent().parent().attr('id');
		var nextPage = pageId == 'page3' ? 'page2' : pageId == 'page2' ? 'page1' : false;
		if(nextPage){
			$('#'+pageId).hide();
			$('#'+nextPage).fadeToggle();
		}



	})

});


