/**
 * query.js: AJAX queries for GAHTC
 */

function gahtcApplication() {}

gahtcApplication.whichToGet = function (sel) {
	if (sel.hasClass( "module" )) {
		var module_id = sel.data( "moduleid" );
		gahtcApplication.getModule(module_id);
	} else if (sel.hasClass( "lecture" )) {
		var lecture_id = sel.data( "lectureid" );
		gahtcApplication.getLecture(lecture_id);
	} else if (sel.hasClass( "lecture_document" )) {
		var lecture_document_id = sel.data( "lecturedocumentid" );
		gahtcApplication.getLectureDocument(lecture_document_id);		
	} else if (sel.hasClass( "lecture_slide" )) {
		var lecture_slide_id = sel.data( "lectureslideid" );
		gahtcApplication.getLectureSlide(lecture_slide_id);
	} else {}
}


gahtcApplication.getModule = function (module_id) {
	$.ajax({
		type: "GET",
		url: "/show_module/" + module_id + "/" ,
		success: function(data){
			$('.searchSidebar').html(data);
			gahtcApplication.updateFooter();
        }
	});
}

gahtcApplication.getLecture = function (lecture_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture/" + lecture_id + "/" ,
		success: function(data){
			$('.searchSidebar').html(data);
			gahtcApplication.updateFooter();
        }
	});		
}

gahtcApplication.getLectureSegment = function (lecture_segment_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture_segment/" + lecture_segment_id + "/" ,
		success: function(data){
			$('.searchSidebar').html(data);
			gahtcApplication.updateFooter();
        }
	});		
}

gahtcApplication.getLectureDocument = function (lecture_document_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture_document/" + lecture_document_id + "/" ,
		success: function(data){
			$('.searchSidebar').html(data);
			gahtcApplication.updateFooter();
        }
	});		
}

gahtcApplication.getLectureSlide = function (lecture_slide_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture_slide/" + lecture_slide_id + "/" ,
		success: function(data){
			$('.searchSidebar').html(data);
			gahtcApplication.updateFooter();
        }
	});
}

gahtcApplication.getLectureModal = function (lecture_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture_modal/" + lecture_id + "/" ,
		success: function(data){
			$('#slideshow').html(data);
			$('#slideshow').modal('show');
        }
	});		
}

gahtcApplication.getLectureSegmentModal = function (lecture_segment_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture_segment_modal/" + lecture_segment_id + "/" ,
		success: function(data){
			$('#slideshow').html(data);
			$('#slideshow').modal('show');
        }
	});		
}

gahtcApplication.getLectureSlideModal = function (lecture_slide_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture_slide_modal/" + lecture_slide_id + "/" ,
		success: function(data){
			$('#slideshow').html(data);
			$('#slideshow').modal('show');
        }
	});		
}

gahtcApplication.createNewBundle = function () {
	// get values
	var title = $(" #newBundleName ").val();
	var itemid = $(" #newBundleName ").data( "itemid" );

	$.ajax({
		type: "GET",
		url: "/create_new_bundle/?title=" + title + "&itemid=" + itemid,
		success: function(data){
			var timeout = window.setTimeout(slowAlert, 300);
			function slowAlert() {
				// success alert message
				$('.bundle-add_alert').removeClass('hidden');
				$('#bundle-title').text(title);
			}

			// add response from template to bundles uls
			$('.bundles').html(data);
			gahtcApplication.updateFooter();
        }
	});

}

gahtcApplication.addToBundle = function (bundle, itemid, title) {
	$.ajax({
		type: "GET",
		url: "/add_to_bundle/?bundle=" + bundle + "&itemid=" + itemid,
		success: function(data){
			// success alert message
			var timeout = window.setTimeout(slowAlert, 300);
			function slowAlert() {
				$('.bundle-add-alert').removeClass('hidden');
				$('#bundle-title').text(title);
			}

        }
	});
}

gahtcApplication.removeFromBundle = function (bundle, itemid, type) {
	$.ajax({
		type: "GET",
		url: "/remove_from_bundle/?bundle=" + bundle + "&itemid=" + itemid + "&type=" + type,
		success: function(data){
			gahtcApplication.getBundle(bundle);
			gahtcApplication.updateFooter();
        }
	});
}

gahtcApplication.getBundle = function (bundle_id) {
	$.ajax({
		type: "GET",
		url: "/show_bundle/" + bundle_id + "/" ,
		success: function(data){
			$('.bundleSidebar').html(data);
			gahtcApplication.updateFooter();
        }
	});
}

gahtcApplication.zipUpBundle = function (bundle_id) {
	$.ajax({
		type: "GET",
		url: "/zip_up_bundle/" + bundle_id + "/" ,
		success: function(data){
			$('#downloadFileArea').html(data);
        }
	});
}

gahtcApplication.zipUpModule = function (module_id) {
	$.ajax({
		type: "GET",
		url: "/zip_up_module/" + module_id + "/" ,
		success: function(data){
			$('#downloadFileArea').html(data);
        }
	});
}

gahtcApplication.zipUpLecture = function (lecture_id) {
	$.ajax({
		type: "GET",
		url: "/zip_up_lecture/" + lecture_id + "/" ,
		success: function(data){
			$('#downloadFileArea').html(data);
        }
	});
}

gahtcApplication.refreshSidebarBundle = function () {
	// refresh list of bundles in the sidebar
	$.ajax({
		type: "GET",
		url: "/refresh_sidebar_bundle/",
		success: function(data){
			// populate bundle list 
			$('.resultsScrollBundle').html(data);
			$( ".bundleResult:first" ).addClass('active');
			// pull data for active bundle into sidebar
			var bundleid = $( ".bundleResult:first" ).data( 'bundleid' );
			if (bundleid) {
				gahtcApplication.getBundle(bundleid);
				gahtcApplication.updateFooter();
			}
        }
	});
}

gahtcApplication.saveSearchString = function (searchString) {
	$.ajax({
		type: "GET",
		url: "/save_search/?searchString=" + keyword,
		success: function(data){
			$('#searchSaved').removeClass('hidden');
			$('.savedSearchList').html(data);
			gahtcApplication.updateFooter();
        }
	});
}

gahtcApplication.saveComment = function (comment, itemid) {
	$.ajax({
		type: "GET",
		url: "/save_comment/?comment=" + comment + "&itemid=" + itemid,
		success: function(data){
			$('.searchSidebar').html(data);
			gahtcApplication.updateFooter();
        }
	});
}

/* on ajax calls, set position of footer */
gahtcApplication.updateFooter = function () {
	var $body = $('body').height();
	var $win = $(window).height();
	console.log($body, 'body');
	console.log($win, 'win');
	if ($body <= $win ) {
		$('.footer').css({ "position": "absolute", "bottom": "0" });
	} else {
		$('.footer').css({ "position": "relative", "bottom": "auto" });
	}
	if ($('.footer').hasClass('hidden')) {
		$('.footer').removeClass('hidden');
	}
}

gahtcApplication.contactBundle = function (bundleid) {
	$.ajax({
		type: "GET",
		url: "/contact_bundle/?bundleid=" + bundleid,
		success: function(data){
			// no reponse
        	}
	});
}

gahtcApplication.dontContactBundle = function (bundleid) {
	$.ajax({
		type: "GET",
		url: "/dont_contact_bundle/?bundleid=" + bundleid,
		success: function(data){
			// no reponse
        }
	});
}

gahtcApplication.contactModule = function (moduleid) {
	$.ajax({
		type: "GET",
		url: "/contact_module/?moduleid=" + moduleid,
		success: function(data){
			// no reponse
        }
	});
}

gahtcApplication.dontContactModule = function (moduleid) {
	$.ajax({
		type: "GET",
		url: "/dont_contact_module/?moduleid=" + moduleid,
		success: function(data){
			// no reponse
        }
	});
}

gahtcApplication.contactLecture = function (lectureid) {
	$.ajax({
		type: "GET",
		url: "/contact_lecture/?lectureid=" + lectureid,
		success: function(data){
			// no reponse
        }
	});
}

gahtcApplication.dontContactLecture = function (lectureid) {
	$.ajax({
		type: "GET",
		url: "/dont_contact_lecture/?lectureid=" + lectureid,
		success: function(data){
			// no reponse
        }
	});
}

