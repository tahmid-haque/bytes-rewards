let animationLock = false, // Ensure synchronous card-swaps
    size = $('#board_size').data('size');
/**
 * Show the card associated by the given goal position.
 *
 * @param {number} i The goal position
 */
function show(i) {
    $('.card')
        .eq(i)
        .slideDown(1000, function () {
            $('.active .reward-progress').hide();
            $('.active').removeClass('active');
            $('.selected').removeClass('selected');
            $('.horizontal').removeClass('horizontal');
            $('.vertical').removeClass('vertical');
            $('.d-diagonal').removeClass('d-diagonal');
            $('.a-diagonal').removeClass('a-diagonal');
            $(`.r${parseInt(i / size)}`).addClass('horizontal');
            $(`.c${i % size}`).addClass('vertical');
            if (i % size === parseInt(i / size))
                $(`.d0`).addClass('d-diagonal');
            if (parseInt(i / size) === size - 1 - (i % size))
                $(`.d1`).addClass('a-diagonal');
            $('#board td').eq(i).addClass('selected');
            $(this).addClass('active');
            animationLock = false;
            $('#hint').slideUp(500);
        });
}

/**
 * Show the goal specified by i after hiding any prior cards.
 *
 * @param {Number} i Index of card to change to
 */
function changeCard(i) {
    if (!animationLock) {
        animationLock = true;
        if ($('.card:visible').length !== 1) show(i);
        else $('.card:visible').slideUp(1000, () => show(i));
        $('#board td').eq(i).addClass('selected');
    }
}

/**
 * Add event listeners to each goal box so that their card shows and the previous card is hidden.
 */
for (let i = 0; i < $('.card').length; i++) {
    $('#board td')
        .eq(i)
        .click(() => changeCard(i));
}

/**
 * Show the user's reward progress in a table given a reward.
 *
 * @param {jQuery} reward The reward row that was clicked
 */
function showRewardProgress(reward) {
    let path = reward.attr('path'),
        rwProgress = $('.active .reward-progress');

    // set reward text for reward table
    $('.active .reward-progress-text')
        .text(reward.children(':last-child').text())
        .attr('style', reward.children(':first-child').attr('style'));

    // add goal information to each row of reward table
    $('.active .goal-progress').each(function (i) {
        let goal = $(`.${path}`).eq(i),
            icon = goal.children('i').hasClass('fa-hamburger')
                ? 'fa-times'
                : 'fa-check',
            completeClass = icon == 'fa-check' ? 'complete' : 'not-complete';

        $(this).off('click');

        // make goals clickable
        $(this).click(function () {
            $('#board td').each(function (index) {
                if ($(this)[0] === goal[0]) changeCard(index);
            });
        });

        // style the x or checkmark
        $(this)
            .children(':last-child')
            .removeClass('complete')
            .removeClass('not-complete')
            .addClass(completeClass);

        // add goal text
        $(this).children(':first-child').text(goal.attr('title'));

        // add goal completion
        $(this)
            .find('.fas')
            .removeClass('fa-check')
            .removeClass('fa-times')
            .addClass(icon);
    });

    // show updated table
    rwProgress.fadeIn(600, () => {
        animationLock = false;
    });
}

/**
 * Add event listeners to all reward rows.
 */
$('.reward-table .reward-path').click(function () {
    if (!animationLock) {
        animationLock = true;

        if ($('.active .reward-progress:visible').length !== 1)
            showRewardProgress($(this));
        else {
            // hide old reward table
            $('.active .reward-progress').fadeOut(600, () =>
                showRewardProgress($(this))
            );
        }
    }
});
