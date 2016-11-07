/**
 * controller.js: listeners and controllers for GAHTC
 */


$( document ).ready(function() {

	// fade in main image and search bar
	$(".fadein").fadeIn("slow");

	// check for the existence of tab
	if (typeof tab === 'undefined' || tab == "none") {
		// do nothing
	} else if (tab == "bundle") {
		$('.nav-tabs a[href="#my-course-bundles"]').tab('show');
	} else if (tab == "profile") {
		$('.nav-tabs a[href="#my-profile"]').tab('show');		
	} else if (tab == "searches") {
		$('.nav-tabs a[href="#my-saved-searches"]').tab('show');		
	}

	// select first in list and populate search result bar
	$( ".result:first" ).addClass('active');
	gahtcApplication.whichToGet($( ".result:first" ));

	// select first in bundle list and pull bundle for right sidebar
	$( ".bundleResult:first" ).addClass('active');
	var bundleid = $( ".bundleResult:first" ).data( 'bundleid' );
	if (bundleid) {
		gahtcApplication.getBundle(bundleid);
	}

	// swap out <em> tags for <strong> tags for search results
	$( ".swapem em").replaceWith(function(){
	    return $("<strong />").append($(this).contents());
	});

	// on click of module, run query to pull module
	$( ".module" ).click(function(e) {
		$( ".result" ).removeClass('active');
		$( this ).addClass('active');
		var module_id = $( this ).data( "moduleid" );
		gahtcApplication.getModule(module_id);
	});

	// on click of lecture, run query to pull lecture
	$( ".lecture" ).click(function(e) {
		$( ".result" ).removeClass('active');
		$( this ).addClass('active');
		var lecture_id = $( this ).data( "lectureid" );
		gahtcApplication.getLecture(lecture_id);
	});

	// on click of lecture-document, run query to pull lecture document
	$( ".lecture_segment" ).click(function(e) {
		$( ".result" ).removeClass('active');
		$( this ).addClass('active');
		var lecture_segment_id = $( this ).data( "lecturesegmentid" );
		gahtcApplication.getLectureSegment(lecture_segment_id);
	});

	// on click of lecture-document, run query to pull lecture document
	$( ".lecture_document" ).click(function(e) {
		$( ".result" ).removeClass('active');
		$( this ).addClass('active');
		var lecture_document_id = $( this ).data( "lecturedocumentid" );
		gahtcApplication.getLectureDocument(lecture_document_id);
	});

	// on click of lecture-document, run query to pull lecture document
	$( ".lecture_slide" ).click(function(e) {
		$( ".result" ).removeClass('active');
		$( this ).addClass('active');
		var lecture_slide_id = $( this ).data( "lectureslideid" );
		gahtcApplication.getLectureSlide(lecture_slide_id);
	});

	// launch modal to show lectures slides
	$(document).on('click', '.launchModal', function(e) {
		e.preventDefault();
        var lecture_id = $( this ).data( "lectureid" );
        gahtcApplication.getLectureModal(lecture_id);
	});

	// launch modal to show lecture segment slides
	$(document).on('click', '.launchSegmentModal', function(e) {
		e.preventDefault();
        var lecture_segment_id = $( this ).data( "lecturesegmentid" );
        gahtcApplication.getLectureSegmentModal(lecture_segment_id);
	});

	// launch modal to show lecture slides
	$(document).on('click', '.launchSlideModal', function(e) {
		e.preventDefault();
        var lecture_slide_id = $( this ).data( "lectureslideid" );
        gahtcApplication.getLectureSlideModal(lecture_slide_id);
	});

	$(document).on('click', '.bundleResult', function(e) {
		e.preventDefault();
		$( ".bundleResult" ).removeClass('active');
		$( this ).addClass('active');
		var bundleid = $( this ).data( 'bundleid' );
		gahtcApplication.getBundle(bundleid);
	});



	$(document).keydown(function(e) {
	    switch(e.which) {
	        case 38: // up
	        if ( $( "#search-results" ).hasClass("active") && $( ".result.active" ).prev().hasClass("result") ) {
				gahtcApplication.whichToGet($( ".result.active" ).prev());
		        $( ".result.active" ).removeClass('active').prev().addClass('active');
		        $(".resultsScroll").scrollTo(".result.active");
	        } else if ( $( "#my-course-bundles" ).hasClass("active") && $( ".bundleResult.active" ).prev().hasClass("bundleResult") ) {
		        $( ".bundleResult.active" ).removeClass('active').prev().addClass('active');
	        	var bundleid = $( ".bundleResult.active" ).data( 'bundleid' );
	        	gahtcApplication.getBundle(bundleid);
	        	$(".resultsScrollBundle").scrollTo(".bundleResult.active");     	
	        }
	        break;

	        case 40: // down
	        if ( $( "#search-results" ).hasClass("active") && $( ".result.active" ).next().hasClass("result") ) {
				gahtcApplication.whichToGet($( ".result.active" ).next());
		        $( ".result.active" ).removeClass('active').next().addClass('active');
		        $(".resultsScroll").scrollTo(".result.active");
	        } else if ( $( "#my-course-bundles" ).hasClass("active") && $( ".bundleResult.active" ).next().hasClass("bundleResult") ) {
		        $( ".bundleResult.active" ).removeClass('active').next().addClass('active');
	        	var bundleid = $( ".bundleResult.active" ).data( 'bundleid' );
	        	gahtcApplication.getBundle(bundleid);
	        	$(".resultsScrollBundle").scrollTo(".bundleResult.active");     	
	        }
	        break;

	        default: return; // exit this handler for other keys
	    }
	    e.preventDefault(); // prevent the default action (scroll / move caret)
	});

	// create new bundle
	$(document).on('click', '.create-new-bundle', function(e) {
		e.preventDefault();
		// open the modal
		$('#newBundleModal').modal('show');
		// pull data value from parent element
		var itemid = $(this).parents( "ul" ).data( "itemid" );
		// add data value to hidden field in modal form
		$("#newBundleName").data( "itemid", itemid );
	});

	// run ajax to create new bundle when save is clicked
	$(" #createNewBundle ").click(function(e) {
		e.preventDefault();
		// check to see if a title was added
		if ($(" #newBundleName ").val().length == 0) {
			$(" #noBundleTitleAlert ").removeClass('hidden');
		} else {
			// run function 
			gahtcApplication.createNewBundle();

			// close the modal
			$('#newBundleModal').modal('hide');

			// update bundle page
			gahtcApplication.refreshSidebarBundle();

		}
	});

	// add to a bundle
	$(document).on('click', '.add-to-bundle', function(e) { 
		e.preventDefault();
		// pull bundle id
		var bundle = $(this).data( "bundle" );
		// pull data value from parent element
		var itemid = $(this).parents( "ul" ).data( "itemid" );
		// set title in alert
		var title = $(this).text();
		// run function
		gahtcApplication.addToBundle(bundle, itemid, title);

		// refresh bundle page
		gahtcApplication.refreshSidebarBundle();
	});

	// remove from a bundle
	$(document).on('click', '.remove-from-bundle', function(e) { 
		e.preventDefault();
		// pull bundle id
		var bundle = $(this).data( "bundleid" );
		// pull data value from parent element
		if ($(this).data( "moduleid" )) {
			var type = 'module';
			var itemid = $(this).data( "moduleid" );
		} else if ($(this).data( "lectureid" )) {
			var type = 'lecture';
			var itemid = $(this).data( "lectureid" );
		} else if ($(this).data( "lecturesegmentid" )) {
			var type = 'lecturesegment';
			var itemid = $(this).data( "lecturesegmentid" );
		} else if ($(this).data( "lecturedocumentid" )) {
			var type = 'lecturedocument';
			var itemid = $(this).data( "lecturedocumentid" );
		} else if ($(this).data( "lectureslideid" )) {
			var type = 'lectureslide';
			var itemid = $(this).data( "lectureslideid" );			
		}
		// run function
		gahtcApplication.removeFromBundle(bundle, itemid, type);

	});

	// switch tab on download button click
	$(" .switchToBundle ").click(function(e) {
		e.preventDefault();
		$('.nav-tabs a[href="#my-course-bundles"]').tab('show');
	});
	

	// download bundle
	$(document).on('click', '.downloadBundle', function(e) { 
		e.preventDefault();
		// open modal
		$('#downloadModal').modal('show');
		// pull bundle id
		var bundle = $(this).data( "bundleid" );
		// run function
		gahtcApplication.zipUpBundle(bundle);

	});

	// download module
	$(document).on('click', '.downloadModule', function(e) { 
		e.preventDefault();
		// open modal
		$('#downloadModal').modal('show');
		// pull bundle id
		var module = $(this).data( "moduleid" );
		// run function
		gahtcApplication.zipUpModule(module);

	});

	// download module
	$(document).on('click', '.downloadLecture', function(e) { 
		e.preventDefault();
		// open modal
		$('#downloadModal').modal('show');
		// pull bundle id
		var lecture = $(this).data( "lectureid" );
		// run function
		gahtcApplication.zipUpLecture(lecture);

	});

	// return to previous html after modal is closed
	$('#downloadModal').on('hidden.bs.modal', function (e) {
		$('#downloadFileArea').html('<div class="containter"><div class="row"><div class="col-md-3"><img class="img-responsive pull-right" src="/static/website/css/images/spiffygif_114x114.gif" /></div><div class="col-md-9"><h2>Zipping Up Your Bundle!</h2></div></div></div>');

	});

	// save search string
	// switch tab on download button click
	$(" #saveSearchString ").click(function(e) {
		e.preventDefault();
		gahtcApplication.saveSearchString();
	});

	// submit comment form
	$(document).on('click', '.submitComment', function(e) {
		e.preventDefault();
        var comment = $( "#id_comment" ).val();
		var itemid = $( this ).data( "itemid" );
        gahtcApplication.saveComment(comment, itemid);
	});	

	// listen for tab clicks and move footer
	$(document).on('click', '.nav-tabs', function(e) {
		gahtcApplication.updateFooter();
	});


});
