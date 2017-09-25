/**
 * application.js: initilizes the GAHTC site
 */

var gahtcApp = null;

// const truncateElementText = (elem) => {
//     let classNameOfElement = $(elem).attr('class');
//     let lectureDescriptionTextLength = 123;
//     let elementText = $(elem).text();

//     if (classNameOfElement === 'lecture-description-text' && elementText.length > 123) {
//         elementText = elementText.substring(0, lectureDescriptionTextLength) + ' ...';
//     }
//     $(elem).text(elementText);

// };



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

    // truncateElementText($('.lecture-description-text'));


    $(window).scroll(() => {
        if ($(this).scrollTop() > 400) {
            $('.scrollToTop').fadeIn();
        } else {
            $('.scrollToTop').fadeOut();
        }
    });

    if ($(this).width() < 768) {
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
        $('.user-nav p').css({
            'color': '#a1a0a1'
        });
        $('.main-content').css({
            'margin-top': '80px'
        });
        $('.navbar-header-holder').css({
            'min-height': '0'
        });            
    }

    $(window).scroll(() => {
        if ($(this).scrollTop() > 146 || $(this).width() < 768) {
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
            $('.user-nav p').css({
                'color': '#a1a0a1'
            }); 
            $('.navbar-header-holder').css({
                'min-height': '0'
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
            $('.user-nav p').css({
                'color': '#ffffff'
            });
            $('.main-content').css({
                'margin-top': '146px'
            }); 
            $('.navbar-header-holder').css({
                'min-height': '110px'
            }); 
            isAsideNavOpen = false;
        }

    });

    if ($(document).width() <= 425) {
        $('.main-nav').css({
            'height': '80px'
        });
    }

    $('.scrollToTop').on('click', () => {
        $('html, body').animate({
            scrollTop: 0
        }, 750);
    });

    $('.showMoreHeader').unbind('click').on('click', function () {
        var el = $(this).parent('.module-title').parent('.panel').find("footer > a");
        var text = el.text();
        let allPanelExpand = $('.panel-expand');
        if (text === 'SHOW MORE') {
            $('.showMore').each(function (index) {
                if ($(this) !== el) {
                    $(this).text('SHOW MORE');
                }
                el.text('SHOW LESS');
            })
            $(this).parent('.module-title').find("a > .closeShowMore").removeClass('hidden');
        } else if (text === 'SHOW LESS') {
            el.text('SHOW MORE');
            $(this).parent('.module-title').find("a > .closeShowMore").addClass('hidden');
        }
    });

    $('.showMore').unbind('click').on('click', function () {
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
            $(this).parent('footer').parent('.panel').find(".module-title > a > .closeShowMore").removeClass('hidden');
        } else if (text === 'SHOW LESS') {
            $(this).text('SHOW MORE')
            $(this).parent('footer').parent('.panel').find(".module-title > a > .closeShowMore").addClass('hidden');
        }
    });

    $('.hamburger-icon').click(() => {
        if (isAsideNavOpen) {
            $('.collapsed-container aside').css({
                'display': 'none'
            });
            $('.hamburger-icon').attr('src', '/static/website/css/images/hamburger_icon_grey.svg');
            isAsideNavOpen = false;
        } else {
            $('.collapsed-container aside').css({
                'display': 'block'
            });
            $('.hamburger-icon').attr('src', '/static/website/css/images/hamburger_icon.svg');
            isAsideNavOpen = true;
        }
    });

    $('.hamburger-icon').mouseenter(() => {    
        $('.hamburger-icon').attr('src', '/static/website/css/images/hamburger_icon.svg');
    });

    $('.hamburger-icon').mouseleave(() => {
        if (!isAsideNavOpen) {
            $('.hamburger-icon').attr('src', '/static/website/css/images/hamburger_icon_grey.svg');
        }
    });

    $('.menu-item > p').unbind('click').on('click', (e) => {
        console.log($(e.currentTarget));
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
