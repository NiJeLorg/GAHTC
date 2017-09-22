/**
 * controller.js: listeners and controllers for GAHTC
 */


$(document).ready(function() {

    // fade in main image and search bar
    $(".fadein").fadeIn("slow");

    // launch modal to show lectures slides
    // $(document).on('mouseenter', '.btn-img-hover-interaction', function(e) {
    //     $(this).children('.button-text-ribbon').css({ opacity: 0.9 });
    // });

    // $(document).on('mouseleave', '.btn-img-hover-interaction', function(e) {
    //     $(this).children('.button-text-ribbon').css({ opacity: 0 });
    // });

    // select first in list and populate search result bar
    // $( ".result:first" ).addClass('active');
    // gahtcApplication.whichToGet($( ".result:first" ));

    // // select first in bundle list and pull bundle for right sidebar
    // $(".bundleResult:first").addClass('active');
    // var bundleid = $(".bundleResult:first").data('bundleid');
    // if (bundleid) {
    //     gahtcApplication.getBundle(bundleid);
    // }

    // swap out <em> tags for <strong> tags for search results
    $(".swapem em").replaceWith(function() {
        return $("<strong />").append($(this).contents());
    });

/*    // on click of module, run query to pull module
    $(".module").click(function(e) {
        $(".result").removeClass('active');
        $(this).addClass('active');
        var module_id = $(this).data("moduleid");
        gahtcApplication.getModule(module_id);
    });

    // on click of lecture, run query to pull lecture
    $(".lecture").click(function(e) {
        $(".result").removeClass('active');
        $(this).addClass('active');
        var lecture_id = $(this).data("lectureid");
        gahtcApplication.getLecture(lecture_id);
    });

    // on click of lecture-document, run query to pull lecture document
    $(".lecture_segment").click(function(e) {
        $(".result").removeClass('active');
        $(this).addClass('active');
        var lecture_segment_id = $(this).data("lecturesegmentid");
        gahtcApplication.getLectureSegment(lecture_segment_id);
    });

    // on click of lecture-document, run query to pull lecture document
    $(".lecture_document").click(function(e) {
        $(".result").removeClass('active');
        $(this).addClass('active');
        var lecture_document_id = $(this).data("lecturedocumentid");
        gahtcApplication.getLectureDocument(lecture_document_id);
    });

    // on click of lecture-document, run query to pull lecture document
    $(".lecture_slide").click(function(e) {
        $(".result").removeClass('active');
        $(this).addClass('active');
        var lecture_slide_id = $(this).data("lectureslideid");
        gahtcApplication.getLectureSlide(lecture_slide_id);
    });*/

    // launch modal to show lectures slides
    $(document).on('click', '.launchModal', function(e) {
        e.preventDefault();
        var lecture_id = $(this).data("lectureid");
        gahtcApplication.getLectureModal(lecture_id);
    });

    $(document).on('click', '.launchModuleDescription', function(e) {
        e.preventDefault();
        var module_id = $(this).data('moduleid');
        gahtcApplication.getModuleDescriptionModal(module_id);
    });

    $(document).on('click', '.launchLectureDescription', function(e) {
        e.preventDefault();
        var lecture_id = $(this).data('lectureid');
        gahtcApplication.getLectureDescriptionModal(lecture_id);
    });

    $(document).on('click', '.launchMemberIntroduction', function(e) {
        e.preventDefault();
        var member_id = $(this).data('memberid');
        gahtcApplication.getMemberFullDescrptionModal(member_id);
    });

    // launch modal to show lecture segment slides
    $(document).on('click', '.launchSegmentModal', function(e) {
        e.preventDefault();
        var lecture_segment_id = $(this).data("lecturesegmentid");
        gahtcApplication.getLectureSegmentModal(lecture_segment_id);
    });

    // launch modal to show lecture slides
    $(document).on('click', '.launchSlideModal', function(e) {
        e.preventDefault();
        var lecture_slide_id = $(this).data("lectureslideid");
        gahtcApplication.getLectureSlideModal(lecture_slide_id);
    });

    $(document).on('click', '.bundleResult', function(e) {
        e.preventDefault();
        $(".bundleResult").removeClass('active');
        $(this).addClass('active');
        // var bundleid = $(this).data('bundleid');
        // gahtcApplication.getBundle(bundleid);
    });



    $(document).keydown(function(e) {
        switch (e.which) {
            case 38: // up
                if ($("#search-results").hasClass("active") && $(".result.active").prev().hasClass("result")) {
                    gahtcApplication.whichToGet($(".result.active").prev());
                    $(".result.active").removeClass('active').prev().addClass('active');
                    $(".resultsScroll").scrollTo(".result.active");
                } else if ($("#my-course-bundles").hasClass("active") && $(".bundleResult.active").prev().hasClass("bundleResult")) {
                    $(".bundleResult.active").removeClass('active').prev().addClass('active');
                    var bundleid = $(".bundleResult.active").data('bundleid');
                    gahtcApplication.getBundle(bundleid);
                    $(".resultsScrollBundle").scrollTo(".bundleResult.active");
                }
                break;

            case 40: // down
                if ($("#search-results").hasClass("active") && $(".result.active").next().hasClass("result")) {
                    gahtcApplication.whichToGet($(".result.active").next());
                    $(".result.active").removeClass('active').next().addClass('active');
                    $(".resultsScroll").scrollTo(".result.active");
                } else if ($("#my-course-bundles").hasClass("active") && $(".bundleResult.active").next().hasClass("bundleResult")) {
                    $(".bundleResult.active").removeClass('active').next().addClass('active');
                    var bundleid = $(".bundleResult.active").data('bundleid');
                    gahtcApplication.getBundle(bundleid);
                    $(".resultsScrollBundle").scrollTo(".bundleResult.active");
                }
                break;

            default:
                return; // exit this handler for other keys
        }
        e.preventDefault(); // prevent the default action (scroll / move caret)
    });

    // create new bundle
    $(document).on('click', '.create-new-bundle', function(e) {
        e.preventDefault();
        // open the modal
        $('#newBundleModal').modal('show');
        // pull data value from parent element
        var itemid = $(this).parents("ul").data("itemid");
        // add data value to hidden field in modal form
        $("#newBundleName").data("itemid", itemid);

    });

    // run ajax to create new bundle when save is clicked or keydown on enter key is pressed
    $(" #createNewBundle ").click(function(e) {
        e.preventDefault();
        createNewBundle();
    });

    $('#newBundleName').keypress(function(e) {
        if (e.which == 13) {
            e.preventDefault();
            createNewBundle();
        }
    });

    function createNewBundle() {
        // check to see if a title was added
        if ($(" #newBundleName ").val().length == 0) {
            $(" #noBundleTitleAlert ").removeClass('hidden');
        } else {
            // run function
            gahtcApplication.createNewBundle();

            // close the modal
            $('#newBundleModal').modal('hide');

        }
    }

    // add to a bundle
    $(document).on('click', '.add-to-bundle', function(e) {
        e.preventDefault();
        // pull bundle id
        var bundle = $(this).data("bundle");
        // pull data value from parent element
        var itemid = $(this).parents("ul").data("itemid");
        // set title in alert
        var title = $(this).text();
        // run function
        gahtcApplication.addToBundle(bundle, itemid, title);

    });

    // remove from a bundle
    $(document).on('click', '.remove-from-bundle', function(e) {
        e.preventDefault();
        // pull bundle id
        var bundle = $(this).data("bundleid");
        // pull data value from parent element
        if ($(this).data("moduleid")) {
            var type = 'module';
            var itemid = $(this).data("moduleid");
        } else if ($(this).data("lectureid")) {
            var type = 'lecture';
            var itemid = $(this).data("lectureid");
        } else if ($(this).data("lecturesegmentid")) {
            var type = 'lecturesegment';
            var itemid = $(this).data("lecturesegmentid");
        } else if ($(this).data("lecturedocumentid")) {
            var type = 'lecturedocument';
            var itemid = $(this).data("lecturedocumentid");
        } else if ($(this).data("lectureslideid")) {
            var type = 'lectureslide';
            var itemid = $(this).data("lectureslideid");
        }
        // run function
        gahtcApplication.removeFromBundle(bundle, itemid, type);

    });

    // remove bundle
    $(document).on('click', '.removeBundle', function(e) {
        e.preventDefault();
        // pull bundle id
        var bundle = $(this).data("bundleid");
        // run function
        gahtcApplication.removeBundle(bundle);

    });

    // remove search
    $(document).on('click', '.removeSearch', function(e) {
        e.preventDefault();
        // pull bundle id
        var search = $(this).data("searchid");
        // run function
        gahtcApplication.removeSearch(search);

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
        var bundle = $(this).data("bundleid");
        // run function
        gahtcApplication.zipUpBundle(bundle);

    });

    // download module
    $(document).on('click', '.downloadModule', function(e) {
        e.preventDefault();
        // open modal
        console.log(e);
        $('#downloadModal').modal('show');
        // pull bundle id
        var module = $(this).data("moduleid");
        // run function
        gahtcApplication.zipUpModule(module);

    });

    // download lecture
    $(document).on('click', '.downloadLecture', function(e) {
        e.preventDefault();
        // open modal
        $('#downloadModal').modal('show');
        // pull bundle id
        var lecture = $(this).data("lectureid");
        // run function
        gahtcApplication.zipUpLecture(lecture);

    });

    // download individual files
    $(document).on('click', '.downloadFile', function(e) {
        e.preventDefault();
        // open modal
        $('#downloadIndividualFile').modal('show');
        // pull file path and file name
        var path = '/media/' + $(this).data("file");
        var filesize = $(this).data("filesize");
        var filename = $(this).data("filename");
        $('.downloadLink').attr('href', path);
        $('.filesize').text(filesize);
        $('.filename').text(filename);
    });    

    // download individual files
    $(document).on('click', '.downloadStaticFile', function(e) {
        e.preventDefault();
        // open modal
        $('#downloadIndividualFile').modal('show');
        // pull file path and file name
        var path = $(this).data("file");
        var filename = $(this).data("filename");
        $('.downloadLink').attr('href', path);
        $('.filename').text(filename);    
    });    

    // listening the terms checkbox
    $(document).on('change', '#terms', function(e) {
        // is the box checked or unchecked
        if ($("#terms").prop('checked') == true) {
            $('#downloadHidden').removeClass('hidden');
        } else {
            $('#downloadHidden').addClass('hidden');
        }
    });

    // listening the contact for bundle checkbox
    $(document).on('change', '#contactBundle', function(e) {
        var bundleid = $(this).data("bundleid");
        // is the box checked or unchecked
        console.log(bundleid);
        if ($("#contactBundle").prop('checked') == true) {
            gahtcApplication.contactBundle(bundleid);
        } else {
            gahtcApplication.dontContactBundle(bundleid);
        }
    });

    // listening the contact for module checkbox
    $(document).on('change', '#contactModule', function(e) {
        var moduleid = $(this).data("moduleid");
        // is the box checked or unchecked
        if ($("#contactModule").prop('checked') == true) {
            gahtcApplication.contactModule(moduleid);
        } else {
            gahtcApplication.dontContactModule(moduleid);
        }
    });

    // listening the contact for lecture checkbox
    $(document).on('change', '#contactLecture', function(e) {
        var lectureid = $(this).data("lectureid");
        // is the box checked or unchecked
        if ($("#contactLecture").prop('checked') == true) {
            gahtcApplication.contactLecture(lectureid);
        } else {
            gahtcApplication.dontContactLecture(lectureid);
        }
    });

    // return to previous html after modal is closed
    $('#downloadModal').on('hidden.bs.modal', function(e) {
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
        var comment = $("#id_comment").val();
        if (!comment) {
            comment = $(this).closest(".comment-form").find('textarea').val();
            console.log(comment);
        }
        var itemid = $(this).data("itemid");
        gahtcApplication.saveComment(comment, itemid);
    });

    // listen for tab clicks and move footer
    // $(document).on('click', '.nav-tabs', function(e) {
    //  gahtcApplication.updateFooter();
    // });


    // pull number for # out of url and open accordian on modules and lectures pages
    var url_after_hash = window.location.hash.substr(1);
    if (url_after_hash.search('heading') != -1) {
        var split = url_after_hash.split("_");
        var url_num = split[1];
        // open accordian
        $('#' + url_num).addClass('in');
    }

    // close the download modal after download link is clicked
    $(document).on('click', '.downloadLink', function(e) {
        $('#downloadModal').modal('hide');
        $('#downloadIndividualFile').modal('hide');
    });


    // remove document type
    $(document).on('click', '.removeDocumentType', function(e) {
        e.preventDefault();
        // pull bundle id
        var doctypeid = $(this).data("doctypeid");
        gahtcApplication.removeDocType(doctypeid);

    });


    // ajax search for profiles
    $('#memberNameLookup').keyup(function(e) {
        if (e.which == 13) {
            e.preventDefault();
        }       
    });  

    $('#memberNameLookup').keyup(function(e) {   
        gahtcApplication.searchMembers();
    });



});
