$('#navbar-placeholder').load('/partials/navbar.html', () => {
    $(window).resize(() => {
        if ($(window).width() < 768) {
            $('.dropdown-menu').removeClass('dropdown-menu-right');
            $('.btn-group button').width($('.container').width());
        } else {
            $('.dropdown-menu').addClass('dropdown-menu-right');
            $('.btn-group button').width('auto');
        }
    });

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
});

$('.bio-pic').height((i) => {
    return $('.bio-pic')[i].width;
});
