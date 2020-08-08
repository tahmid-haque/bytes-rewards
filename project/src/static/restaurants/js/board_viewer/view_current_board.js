/**
 * This file contains the code used to render the current bingo board.
 */

/**
 * Given the size of the board, add the HTML required to the render the bottom row.
 *
 * @param {Number} boardSize size of the bingo board
 * @param {Number} row index of row to be added
 * @param {Array} goals array of goals to be displayed
 * @param {Array} rewards array of rewardss to be displayed
 *
 * @return {String} a string containing the HTML for a single goal row
 */
function addMainRow(boardSize, row, goals, rewards) {
    let mainRow = '<tr>';
    for (let col = 0; col < boardSize; col++) {
        mainRow += `<td class="goal" row=${row} col=${col}`; // generate single goal cell
        if (row === col) {
            mainRow += ' diagDescend=0'; // add tag indicating descending diagonal bingo
        }
        if (col == boardSize - row - 1) {
            mainRow += ' diagAscend=0'; // add tag indicating ascending diagonal bingo
        }
        mainRow += `>${goals[row*boardSize+col]}</td>`;
    }
    // generate single reward cell
    mainRow += `<td class="highlight reward" bingo="row" row=${row}>${rewards[row+1]}</td></tr>`;

    return mainRow;
}

/**
 * Given the size of the board, add the HTML required to the render the bottom row.
 *
 * @param {Number} boardSize size of the bingo board
 * @param {Array} rewards array of rewardss to be displayed
 */
function addBottomRow(boardSize, rewards) {
    let bottomRow = '<tr>';
    for (let col = 0; col < boardSize; col++) {
        // generate single reward cell
        bottomRow += `<td class="highlight reward" bingo="col" col=${col}>${rewards[boardSize+1+col]}</td>`;
    }
    // generate bottom-right diagonal cell
    bottomRow += `<td class="highlight reward" bingo="diagDescend" diagDescend=0>${rewards[rewards.length-1]}</td></tr>`;

    return bottomRow;
}

/**
 * Render the bingo board using the provided size of board.
 *
 * @param {Number} boardSize size of the bingo board
 * @param {Array} goals array of goals to be displayed
 * @param {Array} rewards array of rewardss to be displayed
 * @param {String} name of the bingo board
 * @param {String} date the bingo board expires
 */
function renderBoard(boardSize, goals, rewards, name, date) {
    // add the top row
	let content = `
        <tr>
            <td colspan=${boardSize}>
                <h1>Current Board: ${name}</h1>
				<h2>Expiry Date: ${date}</h2>
            </td>
            <td class="highlight reward" bingo="diagAscend" diagAscend=0>${rewards[0]}</td>
        </tr>
    `;

    for (let i = 0; i < boardSize; i++) {
        // add rows containing goals
        content += addMainRow(boardSize, i, goals, rewards);
    }
    content += addBottomRow(boardSize, rewards); // add bottom row consisting of rewards

    $('#board table').html(content); // render the HTML
}
