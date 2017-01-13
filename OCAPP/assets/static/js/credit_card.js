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

	if (response.error) { // Problem!

		// Show the stripe card validation errors on the form:
		$form.find('.payment-errors').text(response.error.message);
		$form.find('.submit').prop('disabled', false); // Re-enable submission

	} else { // Token was created!

		// Get the token ID:
		var token = response.id;
		console.log(token)
		// Insert the token ID into the form so it gets submitted to the server:
		$form.append($('<input type="hidden" name="stripeToken">').val(token));

	}
	member_cost = $form.find('.member_cost').val()

	$.ajax({
		method:"post",
		data: {"token": token,
				"member_cost":member_cost,
				"_csrf_token": csrf_token_js},
				// CHANGED URL FOR TESTING
		url:"/conferences/"+conf_id+"/members/"+mem_id,
		success:function(data){
			if(data.successful){
				window.location = "conferences/"+conf_id+"/confirmation";
			} else {
				//stripe payment errors
				$(".payment-errors").append(data.errors);
			}	
		},
		//http request/response errors
		error: function(data){}
	})

};




