$(document).ready(function() {
    $(window).scroll(function() {
        var sidebar_height = $('.sidebar').height();
        var window_height = $(window).height();

        // sidebar generally fixed, but it should scroll if too big for the screen
        if (sidebar_height > window_height) {
            var scroll = $(this).scrollTop();
            if (sidebar_height - window_height - scroll > 0) {
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
    });

    // fimxe: in "mobile" view, if you toggle sidebar and then enlarge window, sidebar
    // doesn't come back
    $('button').click(function() {
        // $('.sidebar').toggle()

        // this doesn't change anything:

        if ($('.sidebar').css('display') == 'none') {
            $('.sidebar').css({
                'display': 'block'
            });
        } else {
            $('.sidebar').css({
                'display': 'none'
            });
        }
    });

});
