$('#navbar-placeholder').load('/assets/common/partials/navbar.html', () => {
    setDropdown();
    $(window).resize(setDropdown);

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

function setDropdown() {
    if ($(window).width() < 768) {
        $('.dropdown-menu').removeClass('dropdown-menu-right');
        $('.btn-group button, .dropdown-item').width($('.container').width());
    } else {
        $('.dropdown-menu').addClass('dropdown-menu-right');
        $('.btn-group button, .dropdown-item').width('auto');
    }
}
