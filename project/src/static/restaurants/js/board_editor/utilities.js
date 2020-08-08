/**
 * This file contains all the miscellaneous functions used by the board editor.
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
    $('.droppable.reward').hover(
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
 * Calculate the font size of text that appears on goal/reward cells.
 *
 * @returns {Array} array storing size for normal text and position text
 */
function calcFontSize() {
    let textSize, codeSize;

    switch (boardSize) {
        case 3:
            textSize = 24;
            codeSize = 50;
            break;

        case 4:
            textSize = 21;
            codeSize = 40;
            break;

        default:
            textSize = 18;
            codeSize = 35;
            break;
    }

    return [`${textSize}px`, `${codeSize}px`];
}

/**
 * Resize the text in the provided HTML element to fit within the dimensions.
 *
 * @param {jQuery} e jQuery object containing text that needs resizing
 */
function fixText(e) {
    const fontSizes = calcFontSize();

    e.text(e.attr('title')); // initially add longer text
    e.css('fontSize', fontSizes[0]);

    // if longer text is cut off, use position code instead
    if (e[0].scrollHeight > e[0].offsetHeight) {
        e.text(e.attr('index'));
        e.css('fontSize', fontSizes[1]);
    }
}

/**
 * Align the back, customize buttons to appear on the same row as the clear/save buttons.
 */
function alignButtons() {
    if (
        Math.abs(
            $('#back-customize-container').position().top -
                $('#clear-save-container').position().top
        ) < 1
    )
        return;
    const newMargin =
        parseFloat($('#back-customize-container').css('margin-top')) -
        ($('#back-customize-container').offset().top -
            $('#clear-save-container').offset().top);
    $('#back-customize-container').css('margin-top', newMargin);
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
