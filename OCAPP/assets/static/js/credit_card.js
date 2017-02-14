$(function() {
	var $form = $('#payment-form');
	$form.submit(function(event) {
		// Disable the submit button to prevent repeated clicks:
		$form.find('.submit').prop('disabled', true);

		// Request a token from Stripe:
		Stripe.card.createToken($form, stripeResponseHandler);

		// Prevent the form from being submitted:
		return false;
	});
});
function stripeResponseHandler(status, response) {
	// Grab the form:
	var $form = $('#payment-form');
	var token;
	if (response.error) { // Problem!
		console.log(response.error)
		// Show the stripe card validation errors on the form:
		console.log($('#cc-err'))
		$('#cc-err.error').text(response.error.message);
		$('#cc-err.error').show();
		$form.find('.submit').prop('disabled', false); // Re-enable submission

	} else { // Token was created!

		// Get the token ID:
		token = response.id;
	$.ajax({
		method:"post",
		data: {"stripeToken": token,
				"member_cost":member_cost,
				"_csrf_token": csrf_token_js},
		url:"/conferences/"+conf_id+"/members/"+mem_id, 
		success:function(data){
			console.log('1111', data);
			data=JSON.parse(data)
			console.log('2222', data);
			if(data.successful){
				window.location = "/conferences/"+conf_id+"/confirmation";
			} else {
				console.log(data.errors)
				//stripe payment errors
				$("#cc-err").text(data.errors);
				$("#cc-err").show();
			}	
		},
		//http request/response errors
		error: function(data){console.log(data)}
	})
}

};




