$(document).ready(function(){
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
		if(document.getElementById('other').selected){
			$('#inst-info').slideToggle();
		} else {
			$('#inst-info').slideUp();
		}
	});
	var member = {};
	$(document).on('click', '.continue', function(){
		//run validations based on page div id and validations
			var pageId = $(this).parent().parent().attr('id')
			var validObj = validate(pageId, window[pageId + '_valids']);
			
			//send member object to server if all validations were successful
			if(validObj.allValid) {
				console.log(pageId + ' : ' + 'valid')
				for(var i = 0; i < validObj.validations.length; i++){
					member[validObj.validations[i]['fieldName']] = $('#'+validObj.validations[i]['fieldName']).val();
				}
				var nextPage = pageId == 'page1' ? 'page2' : pageId == 'page2' ? 'page3' : false;
				if(!nextPage){
					
				} else {
					console.log(pageId);
					$('#'+pageId).hide();
					$('#'+nextPage).fadeToggle();
				}
			// 	else {
			// 		$.ajax({
			// 			method: 'POST',
			// 			url: '/members/create',
			// 			data: member
			// 		})
			// 	}
			// //if some validations were unsuccessful, extract messages and display them
			// } else {
			// 	for(var i = 0; i < validObj.validations.length; i++){
			// 		if(!validObj.validations[i]['valid']){
			// 			$('#'+validObj.validations[i]['fieldName']+'Err').innerHTML = validObj.validations[i]['message'];
			// 		}
			// 	}
			// }
		}
	});

});