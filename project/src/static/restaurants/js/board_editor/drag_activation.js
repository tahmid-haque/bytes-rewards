/**
 * This file contains the code used to activate the drag/drop capabilities
 * of all goals/rewards.
 */

$('.draggable').draggable(dragOptions); // activate dragging for goals/rewards

$('.draggable').each(function () {
    $(this).text($(this).attr('title')); // add goal/reward text to boxes
});

// configure goals list to act as a droppable container to discard goals
$('#goals .list').droppable({
    hoverClass: 'placeholder',
    accept: function (e) {
        // accept only goals
        return !e.parent().hasClass('item') && e.hasClass('goal');
    },
    drop: function (evt, ui) {
        $(ui.draggable).detach(); // discard goal
        dropped = true;
    },
});

// configure rewards list to act as a droppable container to discard rewards
$('#rewards .list').droppable({
    hoverClass: 'placeholder',
    accept: function (e) {
        // accept only rewards
        return !e.parent().hasClass('item') && e.hasClass('reward');
    },
    drop: function (evt, ui) {
        $(ui.draggable).detach(); // discard reward
        dropped = true;
    },
});

enableDrops(); // activate board-dropping capability
