/**
 * application.js: initilizes the GAHTC site
 */

var gahtcApp = null;

$(document).ready(function() {

    var gahtcApp = new gahtcApplication();


    console.log(window.location.pathname, 'PATHNAME ');

    if (window.location.pathname === '/') {
        $('footer').css('position', 'fixed');
    } else {
        $('footer').css('position', 'static');
    }

});
