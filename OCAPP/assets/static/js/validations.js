function validate(page, valiArr){
	var valid = true
	console.log(valiArr)
	//loop through validations for fields and apply classes if false
	for (var i=0; i<valiArr.length; i++){
		var name = '#' + valiArr[i]['fieldName'];
		console.log(name)
		valiArr[i]['valid'] = valiArr[i]['validation'](name);
		// console.log('11111' + valiArr[i]['valid'])
		if(valiArr[i]['valid']){
			$(name).removeClass('invalid');
			continue;
		} else {
			console.log('There was a problem with...' + name)
			$(name).addClass('invalid'); 
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
		console.log('Operator must be >, <, or =.');
		return false;
	}
};


