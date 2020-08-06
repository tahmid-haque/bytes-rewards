{
	var size = $('#board_size').data("size");
}

/**
 * Show the card associated by the given goal position.
 *
 * @param {number} i The goal position
 */
function show(i) {
    $('.card')
        .eq(i)
        .slideDown(1000, function () {
            $('.selected').removeClass('selected');
            $('.horizontal').removeClass('horizontal');
            $('.vertical').removeClass('vertical');
            $('.d-diagonal').removeClass('d-diagonal');
            $('.a-diagonal').removeClass('a-diagonal');
            $(`.r${parseInt(i / size)}`).addClass('horizontal');
            $(`.c${i % size}`).addClass('vertical');
            if (i % size === parseInt(i / size)) $(`.d0`).addClass('d-diagonal');
            if (parseInt(i / size) === (size-1) - (i % size))
                $(`.d1`).addClass('a-diagonal');
            $('#board td').eq(i).addClass('selected');
            animationLock = false;
            $('#hint').slideUp(500);
        });
}

let animationLock = false; // Ensure synchronous card-swaps

/**
 * Add event listeners to each goal box so that their card shows and the previous card is hidden.
 */
for (let i = 0; i < $('.card').length; i++) {
    $('#board td')
        .eq(i)
        .click(function () {
            if (!animationLock) {
                animationLock = true;
                if ($('.card:visible').length !== 1) show(i);
                else $('.card:visible').slideUp(1000, () => show(i));
                $('#board td').eq(i).addClass('selected');
            }
        });
}