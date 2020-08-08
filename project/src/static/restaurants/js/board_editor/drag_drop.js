/**
 * This file stores the code implementing the drag/drop functionality of goals & rewards.
 */

let swappedLocation, // stores location of goal/reward that was swapped
    swappedItem, // stores HTML element of swapped goal/reward
    dropped = false; // indicator variable to check successful drop

/**
 * Allow cells on the bingo board to catch dropped goals and rewards.
 */
function enableDrops() {
    dropOptions.accept = function (e) {
        return e.hasClass('goal');
    };

    $('.droppable.goal').droppable(dropOptions); // add functionality to goals

    dropOptions.accept = function (e) {
        return e.hasClass('reward');
    };

    $('.droppable.reward').droppable(dropOptions); // add functionality to rewards
}

/**
 * Fix dropzone element size, font-size and text.
 */
function fixDroppables() {
    $('#board td.droppable').each(function () {
        setSize($(this), cellWidth, cellHeight); // update size of drop zone object
        $(this)
            .children('.draggable')
            .each(function () {
                setSize($(this), cellWidth, cellHeight); // update size of draggable object
                fixText($(this)); // fix text in case of overflow
            });
    });
}

/**
 * Return a goal/reward to their original location in case of invalid drops.
 *
 * @returns {Boolean} true on invalid drop, false otherwise
 */
function revert() {
    let wasDropped = dropped;
    if (!dropped) {
        $(this).data(
            'uiDraggable'
        ).originalPosition = originalLocation.offset(); // restore object to original location
        setTimeout(() => {
            $(this).show(); // unhide un-dragged object
        }, 500);
    }
    dropped = false;
    return !wasDropped;
}

/**
 * Generate a clone of the goal/reward object to allow visible dragging.
 */
function createDraggableClone() {
    var clone = $(this).clone().get(0); // clone the dragged object
    if ($(this).parent().hasClass('droppable')) $(this).hide(); // hide original (un-dragged) object
    return clone;
}

/**
 * Callback function used to prepare a goal/reward for dragging.
 *
 * @param {*} evt placeholder variable (for callback) containing event object
 * @param {*} ui jQuery object containing dragged item
 */
function onDragStart(evt, ui) {
    originalLocation = $(this).parent(); // store start location
    setSize(ui.helper, cellWidth, cellHeight);
    fixText(ui.helper);
    $('.show-bingo').removeClass('show-bingo'); // hide any open achievement path
}

/**
 * Callback function activated when a goal/reward is dropped. Prepare the dropped object for
 * placement.
 *
 * @param {*} evt placeholder variable (for callback) containing event object
 * @param {*} ui jQuery object containing dragged item
 */
function onDrop(evt, ui) {
    let draggable = ui.draggable; // the dragged object
    dropped = true;

    // if an item was swapped temporarily, swap it permanently
    if (
        $(this).children('.draggable:visible:not(.ui-draggable-dragging)')
            .length > 0
    ) {
        e = $(this)
            .children('.draggable:visible:not(.ui-draggable-dragging)')
            .detach();
        if (originalLocation.hasClass('droppable'))
            e.prependTo(originalLocation);
    }

    // attach the dragged item to the drop zone
    e = !originalLocation.hasClass('droppable')
        ? $(draggable).clone().draggable(dragOptions)
        : $(draggable).detach();
    setSize(e, cellWidth, cellHeight)
        .css({ top: 0, left: 0 })
        .prependTo($(this))
        .show();
    fixText(e);

    swappedItem = undefined; // reset the swap
    swappedLocation = undefined;
}

function onMouseOver() {
    // if an item was swapped temporarily, swap it back
    if (swappedItem) {
        swappedItem.detach().prependTo(swappedLocation);
        swappedItem = undefined;
        swappedLocation = undefined;
    }

    // if an item exists in drop zone, swap it temporarily
    if (
        $(this).children('.draggable:visible:not(.ui-draggable-dragging)')
            .length > 0
    ) {
        swappedItem = $(this)
            .children('.draggable:visible:not(.ui-draggable-dragging)')
            .detach();
        swappedLocation = $(this);
        if (originalLocation.hasClass('droppable')) {
            swappedItem.prependTo(originalLocation);
        }
    }
}

function onMouseOut() {
    // if an item was swapped temporarily, swap it back
    if (
        swappedLocation &&
        $(this).position().left === swappedLocation.position().left &&
        $(this).position().top === swappedLocation.position().top
    ) {
        swappedItem.detach().prependTo(swappedLocation);
        swappedItem = undefined;
        swappedLocation = undefined;
    }
}

// set drag/drop options to use above functions
let dragOptions = {
        zIndex: 1000,
        revert: revert,
        helper: createDraggableClone,
        start: onDragStart,
        cursorAt: {
            top: cellHeight / 2,
            left: cellWidth / 2,
        },
        cursor: 'pointer',
    },
    dropOptions = {
        hoverClass: 'placeholder',
        drop: onDrop,
        over: onMouseOver,
        out: onMouseOut,
    };
