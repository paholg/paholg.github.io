var fix_sidebar = function(sideh, winh) {
    if (sideh > winh) {
        var scroll = $(this).scrollTop();
        if (sideh - winh - scroll > 0) {
            $('.sidebar').css({
                'position': 'absolute',
                'top': '0',
                'bottom': 'auto'
            });
        } else {
            $('.sidebar').css({
                'position': 'fixed',
                'top': 'auto',
                'bottom': '0'
            });
        }
    } else {
        $('.sidebar').css({
            'position': 'fixed'
        });
    }
};

$(document).ready(function() {
    var sidebar_height = $('.sidebar').height();
    var window_height = $(window).height();

    // sidebar generally fixed, but it should scroll if too big for the screen
    $(window).resize(function() {
        sidebar_height = $('.sidebar').height();
        window_height = $(window).height();
        fix_sidebar(sidebar_height, window_height);
    });
    $(window).scroll(function() {
        fix_sidebar(sidebar_height, window_height);
    });

    $('button').click(function() {
        $('.sidebar').toggle()
    });
});
