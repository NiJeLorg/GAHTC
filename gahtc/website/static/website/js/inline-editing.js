/**
 * inline-editing.js: allowing for inline editing of titles and names of fields using ajax
 */


$( document ).ready(function() {

	// on click of lecture, run query to pull lecture
	$( ".editable-title" ).click(function(e) {
		var sel = this;
		var field = 'title';
		inlineEdit(sel, field);
	});

	// on click of lecture, run query to pull lecture
	$( ".editable-doc" ).click(function(e) {
		var sel = this;
		var field = 'doc';
		inlineEdit(sel, field);
	});

	function inlineEdit(sel, field) {
		// selectors
		var statictext = $(sel).children('.static');
		var edittext = $(sel).children('.edit');

		// allow editing
		statictext.addClass('hidden');
		edittext.removeClass('hidden');

		// what type of title is this?
		if ($(sel).data( "moduledocid" )) {
			var type = 'moduledoc';
			var itemid = $(sel).data( "moduledocid" );
		} else if ($(sel).data( "lectureid" )) {
			var type = 'lecture';
			var itemid = $(sel).data( "lectureid" );
		} else if ($(sel).data( "lecturesegmentid" )) {
			var type = 'lecturesegment';
			var itemid = $(sel).data( "lecturesegmentid" );
		} else if ($(sel).data( "lecturedocumentid" )) {
			var type = 'lecturedocument';
			var itemid = $(sel).data( "lecturedocumentid" );
		} 

		// listen for keypresses and save when enter is pressed.
		var edittextinput = edittext.children('input');
		edittextinput.unbind().bind("keypress", function(e) {
			if (e.which == 13) {
				//get contents of input
				var new_text = edittextinput.val();

				// for document file names, do a bit of validation
				var valid = true;
				if (field == 'doc' && (type == 'moduledoc' || type == 'lecturedocument')) {
					valid = validate(new_text, 'doc');
				} else if (field == 'doc' && (type == 'lecture' || type == 'lecturesegment')) {
					valid = validate(new_text, 'pptx');
				}

				// stop executing the script if filename isn't valid
				if (!valid) {
					return;
				}
				
				// save contents to database
				var url;
				if (field == 'title') {
					url = "/inline_edit_update_title/?new_text=" + new_text + "&type=" + type + "&itemid=" + itemid
				} else {
					url = "/inline_edit_update_doc/?new_text=" + new_text + "&type=" + type + "&itemid=" + itemid
				}

				$.ajax({
					type: "GET",
					url: url,
					success: function(data){
						console.log(data);
			        }
				});

				// update front end text with new value
				statictext.text(new_text);

				//stop editing
				edittext.addClass('hidden');
				statictext.removeClass('hidden');

			}
		});		
	}

	function validate(new_text, test) {
		var validFilename = /^[a-z0-9_.@()-]+\.[^.]+$/i.test(new_text);
		if (!validFilename) {
			alert('The file name you entered has either spaces or an odd character. Please check the file name and try again.');
			return false;
		}

		if (test == 'doc') {
			var isDocxOrPdf = /\.(docx|pdf)$/i.test(new_text);
			if (!isDocxOrPdf) {
				alert('The file name doesn not end in ".docx" or ".pdf". Please check the file name and try again.');
				return false;
			}
		}
		
		if (test == 'pptx') {
			var isPptx = /\.pptx$/i.test(new_text);
			if (!isPptx) {
				alert('The file name doesn not end in ".pptx". Please check the file name and try again.');
				return false;
			}
		}

		return true;
	
	}


});
