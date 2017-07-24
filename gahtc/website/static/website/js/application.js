/**
 * application.js: initilizes the GAHTC site
 */

var gahtcApp = null;

$(document).ready(function() {

    var gahtcApp = new gahtcApplication();

    if (window.location.pathname === '/') {
        $('footer').css('position', 'fixed');
        $('footer').css('bottom', '0');
        $('footer').css('right', '0');
        $('footer p').css('color', '#fff');
    } else {
        $('footer').css('position', 'static');
    }
});

