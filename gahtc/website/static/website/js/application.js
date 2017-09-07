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

    let gahtcApp = new gahtcApplication(),
        isPanelOpen = false,
        isAsideNavOpen = false;

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

    $(window).scroll(() => {
        let navbarHeight = $('.navbar').height();
        if ($(this).scrollTop() > 146) {
            $('.user-nav .user-profile').css({
                'border-radius': '10%'
            });
            $('.navbar .navigation-links').css({
                'display': 'none'
            });
            $('.uncollapsed-logo').css({
                'opacity': '0'
            });
            $('.collapsed-container').css({
                'opacity': '1'
            });
            $('.navbar-header-holder').css({
                'padding': '0'
            });
            $('.main-nav').css({
                'height': '80px'
            });
        } else {
            $('.collapsed-container aside').css({
                'display': 'none'
            })
            $('.user-nav .user-profile').css({
                'border-radius': '50%'
            });
            $('.navbar .navigation-links').css({
                'display': 'flex'
            });
            $('.uncollapsed-logo').css({
                'opacity': '1'
            });
            $('.collapsed-container').css({
                'opacity': '0'
            });
            $('.navbar-header-holder').css({
                'padding': '15px 0'
            })
            $('.main-nav').css({
                'height': '146px'
            });
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

    $('.hamburger-icon').click(() => {
        if (!isAsideNavOpen) {
            $('.collapsed-container aside').css({
                'display': 'block'
            });
            isAsideNavOpen = true;
        } else {
            $('.collapsed-container aside').css({
                'display': 'none'
            });
            isAsideNavOpen = false;
        }

    });

    $('.menu-item > p').on('click', (e) => {
        if ($(e.currentTarget).hasClass('submenu-open')) {
            $(e.currentTarget).next().css('display', 'none');
            $(e.currentTarget).css({
                'text-decoration': 'none'
            });
            $(e.currentTarget).removeClass('submenu-open');
        } else {
            $(e.currentTarget).next().css('display', 'block');
            $(e.currentTarget).css({
                'text-decoration': 'underline'
            });
            $(e.currentTarget).addClass('submenu-open');
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
