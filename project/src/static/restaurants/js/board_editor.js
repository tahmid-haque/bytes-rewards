let swappedLocation,
    swappedItem,
    dropped = false,
    cellWidth = $('#board').innerWidth() / 6,
    cellHeight = $('#board').innerHeight() / 7;

function fixText(e) {
    e.text(e.attr('title'));
    e.css('fontSize', '18px');

    if (e[0].scrollHeight > e[0].offsetHeight) {
        e.text(e.attr('index'));
        e.css('fontSize', '28px');
    } else e.text(e.attr('title'));
}

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

function fixDroppables() {
    $('td.droppable').each(function () {
        setSize($(this), cellWidth, cellHeight);
        $(this)
            .children('.draggable')
            .each(function () {
                setSize($(this), cellWidth, cellHeight);
                fixText($(this));
            });
    });
}

function setSize(child, width, height) {
    let style = {
        width: width,
        height: height,
    };

    return child.css(style);
}

$('.draggable').each(function () {
    fixText($(this));
    fixDroppables();
});

let dragOptions = {
        zIndex: 1000,
        revert: function (evt, ui) {
            let wasDropped = dropped;
            if (!dropped) {
                $(this).data(
                    'uiDraggable'
                ).originalPosition = originalLocation.offset();
                setTimeout(() => {
                    $(this).show();
                }, 500);
            }
            dropped = false;
            return !wasDropped;
        },
        helper: function (evt) {
            var that = $(this).clone().get(0);
            if ($(this).parent().hasClass('droppable')) $(this).hide();
            return that;
        },
        start: function (evt, ui) {
            originalLocation = $(this).parent();
            setSize(ui.helper, cellWidth, cellHeight);
            fixText(ui.helper);
        },
        cursorAt: {
            top: cellHeight / 2,
            left: cellWidth / 2,
        },
        cursor: 'pointer',
    },
    dropOptions = {
        hoverClass: 'placeholder',
        drop: function (evt, ui) {
            var draggable = ui.draggable;
            var droppable = this;
            dropped = true;

            if (
                $(droppable).children(
                    '.draggable:visible:not(.ui-draggable-dragging)'
                ).length > 0
            ) {
                e = $(droppable)
                    .children('.draggable:visible:not(.ui-draggable-dragging)')
                    .detach();
                if (originalLocation.hasClass('droppable'))
                    e.prependTo(originalLocation);
            }

            e = !originalLocation.hasClass('droppable')
                ? $(draggable).clone().draggable(dragOptions)
                : $(draggable).detach();
            setSize(e, cellWidth, cellHeight)
                .css({ top: 0, left: 0 })
                .prependTo($(droppable))
                .show();
            fixText(e);

            swappedItem = undefined;
            swappedLocation = undefined;
        },
        over: function (evt, ui) {
            var droppable = this;

            if (swappedItem) {
                swappedItem.detach().prependTo(swappedLocation);
                swappedItem = undefined;
                swappedLocation = undefined;
            }

            if (
                $(droppable).children(
                    '.draggable:visible:not(.ui-draggable-dragging)'
                ).length > 0
            ) {
                swappedItem = $(droppable)
                    .children('.draggable:visible:not(.ui-draggable-dragging)')
                    .detach();
                swappedLocation = $(droppable);
                if (originalLocation.hasClass('droppable')) {
                    swappedItem.prependTo(originalLocation);
                }
            }
        },
        out: function (evt, ui) {
            if (
                swappedLocation &&
                $(this).position().left === swappedLocation.position().left &&
                $(this).position().top === swappedLocation.position().top
            ) {
                ('Found a swap item! Detaching and reattaching to swappedLocation!');
                swappedItem.detach().prependTo(swappedLocation);
                swappedItem = undefined;
                swappedLocation = undefined;
            }
        },
    };

$('.draggable').draggable(dragOptions);

dropOptions.accept = function (e) {
    return e.hasClass('goal');
};

$('.droppable.goal').droppable(dropOptions);

dropOptions.accept = function (e) {
    return e.hasClass('reward');
};

$('.droppable.reward').droppable(dropOptions);

$('#goals .list').droppable({
    hoverClass: 'placeholder',
    accept: function (e) {
        return !e.parent().hasClass('item') && e.hasClass('goal');
    },
    drop: function (evt, ui) {
        $(ui.draggable).detach();
        dropped = true;
    },
});

$('#rewards .list').droppable({
    hoverClass: 'placeholder',
    accept: function (e) {
        return !e.parent().hasClass('item') && e.hasClass('reward');
    },
    drop: function (evt, ui) {
        $(ui.draggable).detach();
        dropped = true;
    },
});

$(window).on('resize', () => {
    cellWidth = $('#board').innerWidth() / 6;
    cellHeight = $('#board').innerHeight() / 7;
    fixDroppables();
    alignButtons();
});

$('.droppable.reward').hover(
    function () {
        $(`.${$(this).attr('bingo')}`).addClass('show-bingo');
    },
    function () {
        $(`.${$(this).attr('bingo')}`).removeClass('show-bingo');
    }
);

$('#back').click(function () {
    if (
        confirm(
            'Are you sure you want to leave this page? All unsaved changes will be lost.'
        )
    ) {
        window.location.href = '/';
    }
});

$('#customize').click(function () {
    if (
        confirm(
            'Are you sure you want to leave this page? All unsaved changes will be lost.'
        )
    ) {
        window.location.href = '/customize';
    }
});

$('#clear').click(function () {
    $('td.droppable').empty();
    $('input').val('');
});

$('#save').click(function () {
    let count = 0;
    $('td.droppable').each(function () {
        if ($(this).children().length === 1) count++;
    });
    if (count === 37 && $("input[name='board_name']").val() !== '') {
        $('td .goal').each(function () {
            $('<input />')
                .attr('type', 'hidden')
                .attr('name', 'board[]')
                .attr('value', $(this).attr('key'))
                .appendTo('form');
        });
        $('td .reward').each(function () {
            $('<input />')
                .attr('type', 'hidden')
                .attr('name', 'board_reward[]')
                .attr('value', $(this).attr('key'))
                .appendTo('form');
        });
        $('form').submit();
    } else alert('Please fill all components of the board before saving.');
});
