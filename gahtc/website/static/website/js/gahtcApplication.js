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

gahtcApplication.scrollIntoView = function (element, container) {
	var containerTop = container.scrollTop(); 
	console.log(containerTop);
	var containerBottom = containerTop + container.height(); 
	var elemPos = element.position();
	var elemBottom = elemPos.top + element.height(); 
	console.log(elemPos.top);
	if (elemBottom < containerBottom) {
		container.scrollTop(elemPos.top);
	} 
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



