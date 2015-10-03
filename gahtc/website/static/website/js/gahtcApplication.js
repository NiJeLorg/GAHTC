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
			$('.rightSidebar').html(data);
        }
	});
}

gahtcApplication.getLecture = function (lecture_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture/" + lecture_id + "/" ,
		success: function(data){
			$('.rightSidebar').html(data);
        }
	});		
}

gahtcApplication.getLectureDocument = function (lecture_document_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture_document/" + lecture_document_id + "/" ,
		success: function(data){
			$('.rightSidebar').html(data);
        }
	});		
}

gahtcApplication.getLectureSlide = function (lecture_slide_id) {
	$.ajax({
		type: "GET",
		url: "/show_lecture_slide/" + lecture_slide_id + "/" ,
		success: function(data){
			$('.rightSidebar').html(data);
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
			// success alert message
			$('.bundle-add_alert').removeClass('hidden');
			$('#bundle-title').text(title);

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
			$('.bundle-add-alert').removeClass('hidden');
			$('#bundle-title').text(title);
			console.log($('#bundle-title'));
        }
	});
}


