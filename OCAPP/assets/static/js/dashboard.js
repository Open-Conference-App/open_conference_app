$(document).ready(function(){
	$('.content-table tr').click(function(){
			var id = $(this).children('.data').attr('data-id')
			console.log(id)
			var type = $(this).parent().parent().attr('data-type')
			window.location = '/' + type + '/' + id
	})
})