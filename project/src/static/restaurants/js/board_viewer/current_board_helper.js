/**
 * This file contains all the helper functions used by board viewer.
 */

/**
 * Calculate the width and height of goal/reward cells.
 */
function updateCellHeight() {
    cellWidth = $('#board').innerWidth() / (boardSize + 1);
    cellHeight = $('#board').innerHeight() / (boardSize + 2);
}

/**
 * Add hover functionality to the reward cells so that they indicate their
 * corresponding achievement path.
 */
function addHoverFunctionality() {
    $('.highlight.reward').hover(
        // on mouse over, show the achievement path
        function () {
            const bingo = $(this).attr('bingo'),
                target = `${bingo}=${$(this).attr(`${bingo}`)}`;
            $(`.goal[${target}]`).addClass('show-bingo');
        },
        // on mouse out, hide the achievement path
        function () {
            $('.show-bingo').removeClass('show-bingo');
        }
    );
}

/**
 * Resize an HTML element to the provided width and height.
 *
 * @param {jQuery} element HTML element to resize
 * @param {Number} width target width
 * @param {Number} height target height
 *
 * @returns {jQuery} element that was resized
 */
function setSize(element, width, height) {
    let style = {
        width: width,
        height: height,
    };

    return element.css(style);
}

/**
 * Fix size of the right reward boxes.
 */
function fixSize() {
    $('#board td.highlight').each(function () {
        setSize($(this), cellWidth, cellHeight); // set size of rewards
    });
}
