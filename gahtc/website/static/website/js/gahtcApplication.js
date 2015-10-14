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
        }
	});
}

gahtcApplication.getLecture = function (lecture_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture/" + lecture_id + "/" ,
		success: function(data){
			$('.searchSidebar').html(data);
        }
	});		
}

gahtcApplication.getLectureDocument = function (lecture_document_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture_document/" + lecture_document_id + "/" ,
		success: function(data){
			$('.searchSidebar').html(data);
        }
	});		
}

gahtcApplication.getLectureSlide = function (lecture_slide_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture_slide/" + lecture_slide_id + "/" ,
		success: function(data){
			$('.searchSidebar').html(data);
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
        }
	});
}

gahtcApplication.getBundle = function (bundle_id) {
	$.ajax({
		type: "GET",
		url: "/show_bundle/" + bundle_id + "/" ,
		success: function(data){
			$('.bundleSidebar').html(data);
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
			}
        }
	});
}


