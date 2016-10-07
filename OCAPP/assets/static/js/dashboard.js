

$(document).ready(function(){


	//****toggles the display for menu items****

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

	 $('.first').click(function(){
	  	$('.home').css('display', 'block');
		$('.account_info').css('display', 'none');
		$('.presentations_info').css('display', 'none');
	  })

	 // var test = $('.form').serializeArray()
	 // console.log(test)

	// var dude = jQuery.param({name:'dude', name: 'hello'})
	// console.log(dude)

	 // $('test').serializeObject()

	$('.test').click(function(e){
		 var tests = $('.form').serializeArray()
		 $('.form').trigger('reset');
		 
		 for (test in tests){
			 console.log(tests[test])	
		}
	// 	console.log(e)
	// 	return false;
	 })

	 // $('.logout').click(function(e){
	 // 	$.post('/logout')
	 // })


	//****slideToggles menu options****	

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

})