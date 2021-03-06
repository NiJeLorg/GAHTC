/**
 * query.js: AJAX queries for GAHTC
 */

function gahtcApplication() {}

gahtcApplication.whichToGet = function (sel) {
    if (sel.hasClass("module")) {
        var module_id = sel.data("moduleid");
        gahtcApplication.getModule(module_id);
    } else if (sel.hasClass("lecture")) {
        var lecture_id = sel.data("lectureid");
        gahtcApplication.getLecture(lecture_id);
    } else if (sel.hasClass("lecture_document")) {
        var lecture_document_id = sel.data("lecturedocumentid");
        gahtcApplication.getLectureDocument(lecture_document_id);
    } else if (sel.hasClass("lecture_slide")) {
        var lecture_slide_id = sel.data("lectureslideid");
        gahtcApplication.getLectureSlide(lecture_slide_id);
    } else {}
}



gahtcApplication.getModule = function (module_id) {
    $.ajax({
        type: "GET",
        url: "/show_module/" + module_id + "/",
        success: function (data) {
            $('.searchSidebar').html(data);

        }
    });
}


gahtcApplication.getLecture = function (lecture_id) {
    $.ajax({
        type: "GET",
        url: "/show_lecture/" + lecture_id + "/",
        success: function (data) {
            $('.searchSidebar').html(data);
        }
    });
}


gahtcApplication.getLectureSegment = function (lecture_segment_id) {
    $.ajax({
        type: "GET",
        url: "/show_lecture_segment/" + lecture_segment_id + "/",
        success: function (data) {
            $('.searchSidebar').html(data);
        }
    });
}

gahtcApplication.getLectureDocument = function (lecture_document_id) {
    $.ajax({
        type: "GET",
        url: "/show_lecture_document/" + lecture_document_id + "/",
        success: function (data) {
            $('.searchSidebar').html(data);
        }
    });
}


gahtcApplication.getLectureSlide = function (lecture_slide_id) {
    $.ajax({
        type: "GET",
        url: "/show_lecture_slide/" + lecture_slide_id + "/",
        success: function (data) {
            $('.searchSidebar').html(data);
        }
    });
}

gahtcApplication.getLectureModal = function (lecture_id) {
    $.ajax({
        type: "GET",
        url: "/show_lecture_modal/" + lecture_id + "/",
        success: function (data) {
            $('#slideshow').html(data);
            $('#slideshow').modal('show');
        }
    });
};

gahtcApplication.getModuleDescriptionModal = function (module_id) {
    $.ajax({
        type: 'GET',
        url: '/show_module_description/' + module_id + '/',
        success: function (data) {
            $('#moduleFullDescription').html(data);
            $('#moduleFullDescription').modal('show');
        }
    });
};

gahtcApplication.getLectureDescriptionModal = function (lecture_id) {
    $.ajax({
        type: 'GET',
        url: '/show_lecture_description/' + lecture_id + '/',
        success: function (data) {
            $('#lectureFullDescription').html(data);
            $('#lectureFullDescription').modal('show');
        }
    });
};

gahtcApplication.getMemberFullDescrptionModal = function (member_id) {
    $.ajax({
        type: 'GET',
        url: '/show_member_introduction/' + member_id + '/',
        success: function (data) {
            $('#memberFullIntroduction').html(data);
            $('#memberFullIntroduction').modal('show');
        }
    });
};


gahtcApplication.getLectureSegmentModal = function (lecture_segment_id) {
    $.ajax({
        type: "GET",
        url: "/show_lecture_segment_modal/" + lecture_segment_id + "/",
        success: function (data) {
            $('#slideshow').html(data);
            $('#slideshow').modal('show');
        }
    });
}

gahtcApplication.getLectureSlideModal = function (lecture_slide_id) {
    $.ajax({
        type: "GET",
        url: "/show_lecture_slide_modal/" + lecture_slide_id + "/",
        success: function (data) {
            $('#slideshow').html(data);
            $('#slideshow').modal('show');
        }
    });
}

gahtcApplication.createNewBundle = function () {
    // get values
    var title = $(" #newBundleName ").val();
    var itemid = $(" #newBundleName ").data("itemid");

    $.ajax({
        type: "GET",
        url: "/create_new_bundle/?title=" + title + "&itemid=" + itemid,
        success: function (data) {
            var timeout = window.setTimeout(slowAlert, 300);

            function slowAlert() {
                // success alert message
                $('.bundle-add_alert').removeClass('hidden');
                $('#bundle-title').text(title);
            }

            // add response from template to bundles uls
            $('.bundles').html(data);


            // update bundle page
            gahtcApplication.refreshSidebarBundle();

        }
    });

}

gahtcApplication.addToBundle = function (bundle, itemid, title) {
    $.ajax({
        type: "GET",
        url: "/add_to_bundle/?bundle=" + bundle + "&itemid=" + itemid,
        success: function (data) {
            // success alert message
            window.setTimeout(slowAlert, 10);
            window.setTimeout(removeAlert, 5000);            

            function slowAlert() {
                $('.bundle-add-alert').fadeIn( "slow" );
                $('#bundle-title').text(title);
            }

            function removeAlert() {
                $('.bundle-add-alert').fadeOut( "slow" );
            }

        }
    });
}


gahtcApplication.removeFromBundle = function (bundle, itemid, type) {
    $.ajax({
        type: "GET",
        url: "/remove_from_bundle/?bundle=" + bundle + "&itemid=" + itemid + "&type=" + type,
        success: function (data) {
            gahtcApplication.getBundle(bundle);
        }
    });
}


gahtcApplication.removeBundle = function (bundle) {
    $.ajax({
        type: "GET",
        url: "/remove_bundle/?bundle=" + bundle,
        success: function (data) {
            // set next in list to active and remove the active bundle in the list
            var nextBundle = $(".bundleResult.active").next();
            var prevBundle = $(".bundleResult.active").prev();
            var nextBundleID = nextBundle.data("bundleid");
            var prevBundleID = prevBundle.data("bundleid");

            if (nextBundleID) {
                $(".bundleResult.active").remove();
                nextBundle.addClass('active');
                gahtcApplication.getBundle(nextBundleID);
            } else if (prevBundleID) {
                $(".bundleResult.active").remove();
                prevBundle.addClass('active');
                gahtcApplication.getBundle(prevBundleID);
            } else {
                $(".bundleResult.active").remove();
                $('.bundleSidebar').html('');
            }

            // add response from template to bundles uls
            $('.bundles').html(data);
        }
    });
}


gahtcApplication.removeSearch = function (search) {
    $.ajax({
        type: "GET",
        url: "/remove_search/?search=" + search,
        success: function (data) {
            // update search list
            $('.savedSearchList').html(data);
        }
    });
}

gahtcApplication.removeDocType = function (doctypeid) {
    $.ajax({
        type: "GET",
        url: "/admin_removedoctype/?doctypeid=" + doctypeid,
        success: function (data) {
            console.log('success');
            // update document types list
            console.log(data);
            $('.currentDocTypes').html(data);
        }
    });
}


gahtcApplication.getBundle = function (bundle_id) {
    $.ajax({
        type: "GET",
        url: "/show_bundle/" + bundle_id + "/",
        success: function (data) {
            $('#bundle_'+bundle_id ).html(data);
        }
    });
}

gahtcApplication.zipUpBundle = function (bundle_id) {
    $.ajax({
        type: "GET",
        url: "/zip_up_bundle/" + bundle_id + "/",
        success: function (data) {
            $('#downloadFileArea').html(data);
        }
    });
}

gahtcApplication.zipUpModule = function (module_id) {
    $.ajax({
        type: "GET",
        url: "/zip_up_module/" + module_id + "/",
        success: function (data) {
            $('#downloadFileArea').html(data);
        }
    });
}

gahtcApplication.zipUpLecture = function (lecture_id) {
    $.ajax({
        type: "GET",
        url: "/zip_up_lecture/" + lecture_id + "/",
        success: function (data) {
            $('#downloadFileArea').html(data);
        }
    });
}


gahtcApplication.refreshSidebarBundle = function () {
    // refresh list of bundles in the sidebar
    $.ajax({
        type: "GET",
        url: "/refresh_sidebar_bundle/",
        success: function (data) {
            // populate bundle list
            $('.resultsScrollBundle').html(data);
            $(".bundleResult:first").addClass('active');
            // pull data for active bundle into sidebar
            var bundleid = $(".bundleResult:first").data('bundleid');
            if (bundleid) {
                gahtcApplication.getBundle(bundleid);
            }
        }
    });
}


gahtcApplication.saveSearchString = function (searchString) {
    $.ajax({
        type: "GET",
        url: "/save_search/?searchString=" + keyword,
        success: function (data) {
            // success alert message
            window.setTimeout(slowAlert, 10);
            window.setTimeout(removeAlert, 5000);            

            function slowAlert() {
                $('.saved-search-alert').fadeIn( "slow" );
            }

            function removeAlert() {
                $('.saved-search-alert').fadeOut( "slow" );
            }


        }
    });
}

gahtcApplication.saveComment = function (comment, itemid) {
    $.ajax({
        type: "GET",
        url: "/save_comment/?comment=" + comment + "&itemid=" + itemid,
        success: function (data) {
            if (itemid.startsWith('lecture')) {
                $('.lecture-comments-wrapper').html(data);
            }
            if (itemid.startsWith('module')) {
                var moduleid = itemid.replace('module_','');
                $('#module_comments_'+moduleid).html(data);
            }
        }
    });
}


gahtcApplication.contactBundle = function (bundleid) {
    $.ajax({
        type: "GET",
        url: "/contact_bundle/?bundleid=" + bundleid,
        success: function (data) {
            // no reponse
        }
    });
}

gahtcApplication.dontContactBundle = function (bundleid) {
    $.ajax({
        type: "GET",
        url: "/dont_contact_bundle/?bundleid=" + bundleid,
        success: function (data) {
            // no reponse
        }
    });
}

gahtcApplication.contactModule = function (moduleid) {
    $.ajax({
        type: "GET",
        url: "/contact_module/?moduleid=" + moduleid,
        success: function (data) {
            // no reponse
        }
    });
}

gahtcApplication.dontContactModule = function (moduleid) {
    $.ajax({
        type: "GET",
        url: "/dont_contact_module/?moduleid=" + moduleid,
        success: function (data) {
            // no reponse
        }
    });
}

gahtcApplication.contactLecture = function (lectureid) {
    $.ajax({
        type: "GET",
        url: "/contact_lecture/?lectureid=" + lectureid,
        success: function (data) {
            // no reponse
        }
    });
}

gahtcApplication.dontContactLecture = function (lectureid) {
    $.ajax({
        type: "GET",
        url: "/dont_contact_lecture/?lectureid=" + lectureid,
        success: function (data) {
            // no reponse
        }
    });
}


gahtcApplication.searchMembers = function () {
    // get values
    var keyword = $('#memberNameLookup').val();

    $.ajax({
        type: "GET",
        url: "/search_members/?keyword=" + keyword,
        success: function (data) {
            // retrun the matched profiles to the template
            $('.profiles_returned').html(data);
        }
    });

}

