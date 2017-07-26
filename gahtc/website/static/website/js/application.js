/**
 * application.js: initilizes the GAHTC site
 */

var gahtcApp = null;

const truncateElementText = (elem) => {
    let classNameOfElement = $(elem).attr('class');
    let lectureDescriptionTextLength = 123;
    let elementText = $(elem).text();

    if (classNameOfElement === 'lecture-description-text' && elementText.length > 123) {
        console.log('ola')
        elementText = elementText.substring(0, lectureDescriptionTextLength) + ' ...';
        console.log(elementText);
    }
    $(elem).text(elementText);
};


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

    truncateElementText($('.lecture-description-text'));
});
