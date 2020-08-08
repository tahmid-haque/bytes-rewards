/**
 * This file contains the code used to activate the buttons along the bottom of the
 * bingo board editor.
 */

/**
 * Activate the back button to redirect the user to the previous page when clicked.
 */
$('#back').click(function () {
    if (
        confirm(
            // get user confirmation
            'Are you sure you want to leave this page? All unsaved changes will be lost.'
        )
    ) {
        window.location.href = current_expiry ? '/board' : '/'; // redirect user
    }
});

/**
 * Activate the customize button to redirect the user to the customization page when clicked.
 */
$('#customize').click(function () {
    if (
        confirm(
            // get user confirmation
            'Are you sure you want to leave this page? All unsaved changes will be lost.'
        )
    ) {
        window.location.href = '/customize'; // redirect user
    }
});

/**
 * Clear the board editor of all user data.
 */
$('#clear').click(function () {
    $('td.droppable').empty(); // erase the board
    $('input').val(''); // empty the title, expiry date
});

/**
 * When clicking the save button, gather all user data, validate it and submit to the server.
 */
$('#save').click(function () {
    const requiredCount = boardSize * (boardSize + 2) + 2; // calculate number of boxes
    let count = 0;
    $('td.droppable').each(function () {
        if ($(this).children().length === 1) count++; // count filled goals/rewards
    });

    // validate that all user data was filled
    if (
        count === requiredCount &&
        $("input[name='board_name']").val() !== '' &&
        $("input[name='expiration']").val() !== ''
    ) {
        // prepare goal data for submission
        $('td .goal').each(function () {
            $('<input />')
                .attr('type', 'hidden')
                .attr('name', 'board[]')
                .attr('value', $(this).attr('key'))
                .appendTo('form');
        });

        // prepare reward data for submission
        $('td .reward').each(function () {
            $('<input />')
                .attr('type', 'hidden')
                .attr('name', 'board_reward[]')
                .attr('value', $(this).attr('key'))
                .appendTo('form');
        });

        // prepare board size data for submission
        $('<input />')
            .attr('type', 'hidden')
            .attr('name', 'size')
            .attr('value', boardSize)
            .appendTo('form');
        $('form').submit();

        // alert user of incomplete data
    } else alert('Please fill all components of the board before saving.');
});
