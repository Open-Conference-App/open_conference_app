$(document).ready(function(){
	var user;
	$('button').click(function(){
		var id = $(this).attr('data-id');
		var other = id == 'login' ? 'register' : 'login';
		$('#show-' + id).hide();
		$('#' + other + '-form').hide();
		$('#' + id + '-form').slideToggle();
		$('#show-' + other).slideToggle();
	});

	$('#institution').change(function(){
		if(document.getElementById('other').selected){
			$('#inst-info').slideToggle();
		} else {
			$('#inst-info').slideUp();
		}
	});

	$('.continue').click(function(){
		if($(this).parent().parent().attr('id') == 'page1'){
			if($('#first_name').val().length < 1){
				$('#first_name').addClass('is-danger');
			} else if($('#last_name').val().length < 1){
				$('#last_name').addClass('is-danger');
			} else if($('#email'))

			else {
				user = {
					'first_name': $('#first_name').val(),
					'last_name': $('#last_name').val(),
					'email': $('#email').val(),
					'password': $('#password').val(),
					'confirm-password': $('#confirm-password').val()		
				}
			}

		}
	});

});