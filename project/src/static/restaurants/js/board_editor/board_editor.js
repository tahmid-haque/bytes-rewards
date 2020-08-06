/**
 * This file contains the miscellaneous code used to implement/activate all other functionality
 * in the board editor. This includes the date picker, the board size toggle and board
 * hover functionality.
 */

$(`[size=${boardSize}]`).addClass('current-size'); // hgihlight the current board size

/**
 * Implements size toggle functionality. Activates when the board size is changed.
 */
$('#size-container div').click(function () {
    if ($(this).hasClass('current-size')) return; // prevent clicking current size

    if (
        // get user confirmation
        !confirm(
            'Changing size will erase unsaved changes. Would you like to continue?'
        )
    ) {
        return;
    }
    const clicked = $(this);

    boardSize = Number($(this).attr('size')); // set new board size
    updateCellHeight();
    $('#board').slideUp(function () {
        $('td.droppable').empty(); // erase current goals/rewards on board
        renderBoard(boardSize); // re-render the board
        enableDrops();
        addHoverFunctionality();
        fixDroppables();
        $(this).slideDown(() => {
            alignButtons();
            $('.current-size').removeClass('current-size'); // highlight updated board size
            clicked.addClass('current-size');
        });
    });
});

/**
 * Activates the expiry date input to become a date selector.
 */
$('#date-label-container input').datepicker({
    showAnim: 'slideDown',
    showOtherMonths: true,
    selectOtherMonths: true,
    changeMonth: true,
    changeYear: true,
    minDate: current_expiry || 1,
    defaultDate: 1,
});

if (future_expiry)
    // set the expiration date shown based on user data
    $('#date-label-container input').datepicker('setDate', future_expiry);

addHoverFunctionality();

// on window resize, fix page alignment/format
$(window).on('resize', () => {
    updateCellHeight();
    fixDroppables();
    alignButtons();
});
