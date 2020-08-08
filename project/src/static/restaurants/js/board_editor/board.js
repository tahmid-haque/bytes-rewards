/**
 * This file contains the code used to render the bingo board.
 */

/**
 * Given the size of the board, add the HTML required to the render the bottom row.
 *
 * @param {Number} boardSize size of the bingo board
 * @param {Number} row index of row to be added
 *
 * @return {String} a string containing the HTML for a single goal row
 */
function addMainRow(boardSize, row) {
    let mainRow = '<tr>';
    for (let col = 0; col < boardSize; col++) {
        mainRow += `<td class="droppable goal" row=${row} col=${col}`; // generate single goal cell
        if (row === col) {
            mainRow += ' diagDescend=0'; // add tag indicating descending diagonal bingo
        }
        if (col == boardSize - row - 1) {
            mainRow += ' diagAscend=0'; // add tag indicating ascending diagonal bingo
        }
        mainRow += `></td>`;
    }
    // generate single reward cell
    mainRow += `<td class="droppable reward" bingo="row" row=${row}></td></tr>`;

    return mainRow;
}

/**
 * Given the size of the board, add the HTML required to the render the bottom row.
 *
 * @param {Number} boardSize size of the bingo board
 */
function addBottomRow(boardSize) {
    let bottomRow = '<tr>';
    for (let col = 0; col < boardSize; col++) {
        // generate single reward cell
        bottomRow += `<td class="droppable reward" bingo="col" col=${col}></td>`;
    }
    // generate bottom-right diagonal cell
    bottomRow += `<td class="droppable reward" bingo="diagDescend" diagDescend=0></td></tr>`;

    return bottomRow;
}

/**
 * Render the bingo board using the provided size of board.
 *
 * @param {Number} boardSize size of the bingo board
 */
function renderBoard(boardSize) {
    // add the top row
    let content = `
        <tr>
            <td colspan=${boardSize}>
                <h1>Board Editor</h1>
            </td>
            <td class="droppable reward" bingo="diagAscend" diagAscend=0></td>
        </tr>
    `;

    for (let i = 0; i < boardSize; i++) {
        // add rows containing goals
        content += addMainRow(boardSize, i);
    }
    content += addBottomRow(boardSize); // add bottom row consisting of rewards

    $('#board table').html(content); // render the HTML
}
