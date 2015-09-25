/**
 * query.js: AJAX queries for GAHTC
 */

$( document ).ready(function() {

	// on click of module, run query to pull module
	$( ".module" ).click(function() {
		var module_id = $( this ).data( "moduleid" );
		$.ajax({
			type: "GET",
			url: "/show_module/" + module_id + "/" ,
			success: function(data){
				$('.rightSidebar').html(data);
				console.log(data);
	        }
		});
	});

	// on click of lecture, run query to pull lecture
	$( ".lecture" ).click(function() {
		var lecture_id = $( this ).data( "lectureid" );
		$.ajax({
			type: "GET",
			url: "/show_lecture/" + lecture_id + "/" ,
			success: function(data){
				$('.rightSidebar').html(data);
				console.log(data);
	        }
		});
	});

	// on click of lecture-document, run query to pull lecture document
	$( ".lecture_document" ).click(function() {
		var lecture_document_id = $( this ).data( "lecturedocumentid" );
		$.ajax({
			type: "GET",
			url: "/show_lecture_document/" + lecture_document_id + "/" ,
			success: function(data){
				$('.rightSidebar').html(data);
				console.log(data);
	        }
		});
	});

	// on click of lecture-document, run query to pull lecture document
	$( ".lecture_slide" ).click(function() {
		console.log(this);
		var lecture_slide_id = $( this ).data( "lectureslideid" );
		$.ajax({
			type: "GET",
			url: "/show_lecture_slide/" + lecture_slide_id + "/" ,
			success: function(data){
				$('.rightSidebar').html(data);
				console.log(data);
	        }
		});
	});

});

