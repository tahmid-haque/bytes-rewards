$('#navbar-placeholder').load('/partials/navbar.html');

$(window)
    .bind('resize', function () {
        if ($(this).width() < 768) {
            $('.dropdown-menu').removeClass('dropdown-menu-right');
            $('.btn-group button').width('92vw');
        } else {
            $('.dropdown-menu').addClass('dropdown-menu-right');
            $('.btn-group button').width('auto');
        }
    })
    .trigger('resize');

const navHeight = $('#navbar').height();

$(document).scroll(function () {
    $('.list-group-item').removeClass('active');
    if ($(this).scrollTop() > navHeight) {
        $('.light-nav-item')
            .removeClass('light-nav-item')
            .addClass('dark-nav-item');
        $('#navbar').addClass('pink');
    } else {
        $('.dark-nav-item')
            .removeClass('dark-nav-item')
            .addClass('light-nav-item');
        $('#navbar').removeClass('pink');
    }
});
