

$(document).ready(function(){

  //**** slideToggles menu options ****	
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

	$('.presentations, .account, .conferences, .contact, .institution, .conference').css('cursor', 'pointer')
	

  //**** toggles the display for menu items ****
	$('.presentations').click(function(){
		$('.home').css('display', 'none');
		$('.presentations_info').css('display', 'block');
		$('.account_info').css('display', 'none');
	})
	// $('.account').click(function(){
	// 	$('.home').css('display', 'none');
	// 	$('.account_info').css('display', 'block');
	// 	$('.presentations_info').css('display', 'none');
	// })

	 $('.current_conference').click(function(){
	  	$('.home').css('display', 'block');
		$('.account_info').css('display', 'none');
		$('.presentations_info').css('display', 'none');
	})
	$('.edit').click(function(){
	  	$('.account_info').css('display', 'block');
	  	$('.contact_info').css('display', 'block');
	  	$('.membership').css('display', 'none');
	  	$('.conference_info').css('display', 'none');
	  	$('.institution_info').css('display', 'none');
		$('.home').css('display', 'none');
		$('.presentations_info').css('display', 'none');
	})

	$('.payment').click(function(){
	  	$('.membership').css('display', 'block');
	  	$('.conference_info').css('display', 'none');
	  	$('.contact_info').css('display', 'none');
	  	$('.institution_info').css('display', 'none');
	  	$('.account_info').css('display', 'block');
		$('.home').css('display', 'none');
		$('.presentations_info').css('display', 'none');
	})	
  
  //**** profile items toggle display ****
  	$('.contact').click(function(){
	  	$('.contact_info').css('display', 'block');
		$('.institution_info').css('display', 'none');
		$('.conference_info').css('display', 'none');
	})
	$('.institution').click(function(){
	  	$('.contact_info').css('display', 'none');
		$('.institution_info').css('display', 'block');
		$('.conference_info').css('display', 'none');
	})
	$('.conference').click(function(){
	  	$('.contact_info').css('display', 'none');
		$('.institution_info').css('display', 'none');
		$('.conference_info').css('display', 'block');
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


	
})