/**
 * application.js: initilizes the GAHTC site
 */

var gahtcApp = null;

const truncateElementText = (elem) => {
    let classNameOfElement = $(elem).attr('class');
    let lectureDescriptionTextLength = 123;
    let elementText = $(elem).text();

    if (classNameOfElement === 'lecture-description-text' && elementText.length > 123) {
        elementText = elementText.substring(0, lectureDescriptionTextLength) + ' ...';
    }
    $(elem).text(elementText);

};



$(document).ready(function () {

    var gahtcApp = new gahtcApplication();

    let isPanelOpen = false;

    if (window.location.pathname === '/') {
        $('footer').css('position', 'fixed');
        $('footer').css('bottom', '0');
        $('footer').css('right', '0');
        $('footer p').css('color', '#fff');
    } else {
        $('footer').css('position', 'static');
    }

    truncateElementText($('.lecture-description-text'));

    $(window).scroll(() => {
        if ($(this).scrollTop() > 400) {
            $('.scrollToTop').fadeIn();
        } else {
            $('.scrollToTop').fadeOut();
        }
    });

    $('.scrollToTop').on('click', () => {
        $('html, body').animate({
            scrollTop: 0
        }, 750);
    });

    $('.showMore').on('click', function () {
        var text = $(this).text();
        let allPanelExpand = $('.panel-expand');
        if (text === 'SHOW MORE') {
            var el = $(this);
            $('.showMore').each(function (index) {
                if ($(this) !== el) {
                    $(this).text('SHOW MORE');
                }
                el.text('SHOW LESS')
            })
        } else if (text === 'SHOW LESS') {
            $(this).text('SHOW MORE')
        }
    });


    function horizontalScroll() {
        let pos = 0;

        $('.scrollRight').on('click', () => {
            $('.featured-modules').animate({
                scrollLeft: (pos += 400)
            });
        });

        $('.scrollLeft').on('click', () => {
            pos -= 440;
            if (pos < 0) {
                pos = 0;
            }
            $('.featured-modules').animate({
                scrollLeft: pos
            });
        });

    }

    horizontalScroll();

});
