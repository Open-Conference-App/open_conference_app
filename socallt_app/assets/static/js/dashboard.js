

$(document).ready(function(){

	$('.presentations, .account, .conferences').css('cursor', 'pointer')

	$('.presentations').click(function(){
		$('.home').css('display', 'none');
		$('.presentations_info').css('display', 'block');
		$('.account_info').css('display', 'none');
	})
	$('.account').click(function(){
		$('.home').css('display', 'none');
		$('.account_info').css('display', 'block');
		$('.presentations_info').css('display', 'none');
	})

		$('.conferences').mouseenter(function(){
	        $('.sub_conferences').slideDown('medium');
	  }), $('.conferences').mouseleave(function(){
	        $('.sub_conferences').slideUp('medium');
		  });

		$('.account').mouseenter(function(){
	        $('.sub_account').slideDown('medium');
	  }), $('.account').mouseleave(function(){
	        $('.sub_account').slideUp('medium');
		  });

	  $('.first').click(function(){
	  	$('.home').css('display', 'block');
		$('.account_info').css('display', 'none');
		$('.presentations_info').css('display', 'none');
	  })

})