/**
 * controller.js: listeners and controllers for GAHTC
 */


$( document ).ready(function() {

	// fade in main image and search bar
	$(".fadein").fadeIn("slow");

	// select first in list and populate search result bar
	$( ".searchResult:first" ).addClass('active');
	gahtcApplication.whichToGet($( ".searchResult:first" ));

	// on click of module, run query to pull module
	$( ".module" ).click(function() {
		$( ".searchResult" ).removeClass('active');
		$( this ).addClass('active');
		var module_id = $( this ).data( "moduleid" );
		gahtcApplication.getModule(module_id);
	});

	// on click of lecture, run query to pull lecture
	$( ".lecture" ).click(function() {
		$( ".searchResult" ).removeClass('active');
		$( this ).addClass('active');
		var lecture_id = $( this ).data( "lectureid" );
		gahtcApplication.getLecture(lecture_id);
	});

	// on click of lecture-document, run query to pull lecture document
	$( ".lecture_document" ).click(function() {
		$( ".searchResult" ).removeClass('active');
		$( this ).addClass('active');
		var lecture_document_id = $( this ).data( "lecturedocumentid" );
		gahtcApplication.getLectureDocument(lecture_document_id);
	});

	// on click of lecture-document, run query to pull lecture document
	$( ".lecture_slide" ).click(function() {
		$( ".searchResult" ).removeClass('active');
		$( this ).addClass('active');
		var lecture_slide_id = $( this ).data( "lectureslideid" );
		gahtcApplication.getLectureSlide(lecture_slide_id);
	});


	$(document).keydown(function(e) {
	    switch(e.which) {
	        case 38: // up
	        if ( $( ".searchResult.active" ).prev().hasClass("searchResult") ) {
				gahtcApplication.whichToGet($( ".searchResult.active" ).prev());
		        $( ".searchResult.active" ).removeClass('active').prev().addClass('active');
		        $(".searchResultsScroll").scrollTo(".searchResult.active");
	        }
	        break;

	        case 40: // down
	        if ( $( ".searchResult.active" ).next().hasClass("searchResult") ) {
				gahtcApplication.whichToGet($( ".searchResult.active" ).next());
		        $( ".searchResult.active" ).removeClass('active').next().addClass('active');
		        $(".searchResultsScroll").scrollTo(".searchResult.active");
	        }
	        break;

	        default: return; // exit this handler for other keys
	    }
	    e.preventDefault(); // prevent the default action (scroll / move caret)
	});


});
