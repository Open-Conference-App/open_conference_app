$(document).ready(function(){
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

	$('#institution').change(function(){
		if(document.getElementById('other').selected){
			$('#inst-info').slideToggle();
		} else {
			$('#inst-info').slideUp();
		}
	});

	$(document).on('click', '.continue', function(){
		console.log('test')
		//if the clicked element is part of page 1...
		if($(this).parent().parent().attr('id') == 'page1'){
			var email_patt = new RegExp($('#email').pattern);
			var is_valid = true;
			console.log($('#email').val())
			console.log(email_patt.test($('#email').val()))

			if($('#first_name').val().length < 1){
				console.log('first')
				$('#first_name').addClass('is-danger');
				is_valid = false;
			} else {
				$('#first_name').removeClass('is-danger');
			}

			if($('#last_name').val().length < 1){
				console.log('last')
				$('#last_name').addClass('is-danger');
				is_valid = false;
			} else {
				$('#last_name').removeClass('is-danger');
			}

			if(!email_patt.test($('#email').val()) || !$('#email').val()){
				console.log('email')
				$('#email').addClass('is-danger');
				is_valid = false;
			} else {
				$('#email').removeClass('is-danger');
			}
 
			if($('#password').val().length < 9){
				console.log('pass')
				$('#password').addClass('is-danger');
				is_valid = false;
			} else {
				$('#password').removeClass('is-danger');
			}

			if($('#password').val() != $('#confirm-password').val()){
				$('#password').addClass('is-danger');
				$('#confirm-password').addClass('is-danger');
				is_valid = false;
			} else {
				$('#password').removeClass('is-danger');
				$('#confirm-password').removeClass('is-danger');
			}
			console.log('is_valid' + is_valid)

			if(is_valid) {
				user = {
					'first_name': $('#first_name').val(),
					'last_name': $('#last_name').val(),
					'email': $('#email').val(),
					'password': $('#password').val(),
					'confirm-password': $('#confirm-password').val()		
				}
				$('#page1').hide();
				$('#page2').fadeToggle();
			} else {console.log('made it')}
		//else, if the element is part of page 2...
		} else if($(this).parent().parent().attr('id') == 'page2'){
			var is_valid = true;
			if($('#street1').val().length == 0){
				console.log('first')
				$('#street1').addClass('is-danger');
				is_valid = false;
			} else {
				$('#street1').removeClass('is-danger');
			}

			if($('#city').val().length == 0){
				$('#city').addClass('is-danger');
				is_valid = false;
			} else {
				$('#city').removeClass('is-danger');
			}

			if($('#zip').val().length < 5){
				$('#zip').addClass('is-danger');
				is_valid = false;
			} else {
				$('#zip').removeClass('is-danger');
			}

			if(is_valid){
				user['street1'] = $('#street1').val(),
				user['street2'] = $('#street2').val(),
				user['city'] = $('#city').val(),
				user['state'] = $('#state').val(),
				user['zip'] = $('#zip').val()		
			}
			$('#page2').hide();
			$('#page3').fadeToggle();
		} else if($(this).parent().parent().attr('id') == 'page3'){
			$.ajax('/')
		}
	});

});