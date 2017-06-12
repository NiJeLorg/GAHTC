/**
 * inline-editing.js: allowing for inline editing of titles and names of fields using ajax
 */


$( document ).ready(function() {

	// on click of lecture, run query to pull lecture
	$( ".editable-title" ).click(function(e) {
		// selectors
		var statictext = $(this).children('.static');
		var edittext = $(this).children('.edit');

		// allow editing
		statictext.addClass('hidden');
		edittext.removeClass('hidden');

		// what type of title is this?
		if ($(this).data( "moduledocid" )) {
			var type = 'moduledoc';
			var itemid = $(this).data( "moduledocid" );
		} else if ($(this).data( "lectureid" )) {
			var type = 'lecture';
			var itemid = $(this).data( "lectureid" );
		} else if ($(this).data( "lecturesegmentid" )) {
			var type = 'lecturesegment';
			var itemid = $(this).data( "lecturesegmentid" );
		} else if ($(this).data( "lecturedocumentid" )) {
			var type = 'lecturedocument';
			var itemid = $(this).data( "lecturedocumentid" );
		} 

		// listen for keypresses and save when enter is pressed.
		var edittextinput = edittext.children('input');
		edittextinput.keypress(function(e) {
			if (e.which == 13) {
				//get contents of input
				var new_text = edittextinput.val();

				// save contents to database
				$.ajax({
					type: "GET",
					url: "/inline_edit_update_title/?new_text=" + new_text + "&type=" + type + "&itemid=" + itemid,
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

	});

	function updateTitle(new_text, type, itemid) {

	}


});
