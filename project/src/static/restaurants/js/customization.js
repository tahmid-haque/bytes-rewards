/*
    Dynamically update height of the delete button so that it matches the height
    of its containing list item.
*/
function fixGoalHeights() {
    document.querySelectorAll('li').forEach((li) => {
        deleteIcon = li.getElementsByClassName('delete')[0];
        goal = li.getElementsByClassName('goal')[0];
        height = `${goal.getBoundingClientRect().height}px`;
        deleteIcon.style.height = height;
        deleteIcon.style.lineHeight = height;
    });
}

function fixRewardHeights() {
    document.querySelectorAll('li').forEach((li) => {
        deleteIcon = li.getElementsByClassName('delete-reward')[0];
        reward = li.getElementsByClassName('reward')[0];
        height = `${reward.getBoundingClientRect().height}px`;
        deleteIcon.style.height = height;
        deleteIcon.style.lineHeight = height;
    });
}

// Fix delete button height on hover
document.querySelectorAll('.goal').forEach((goal) => {
    goal.addEventListener('mouseenter', () => setTimeout(fixGoalHeights, 450));
    goal.addEventListener('mouseout', () => setTimeout(fixGoalHeights, 450));
});

// Toggle the visibility of the add goal input box
document.querySelector('h1[name="goal"] i').onclick = () => {
    document.querySelector('input[name="goal"]').classList.toggle('hidden-input');
    document.querySelector('form[id="goal"]').classList.toggle('hidden-input');
};

document.querySelector('h1[name="reward"] i').onclick = () => {
    document.querySelector('input[name="reward"]').classList.toggle('hidden-input');
    document.querySelector('form[id="reward"]').classList.toggle('hidden-input');
};

// Submit the delete form
document.querySelectorAll('.delete').forEach((e) => {
    e.onclick = () => {
        form = e.parentElement.children[0];
        if (confirm('Are you sure you want to delete this goal?'))
            form.submit();
    };
});

// Fix delete button height on hover
document.querySelectorAll('.reward').forEach((reward) => {
    reward.addEventListener('mouseenter', () => setTimeout(fixRewardHeights, 450));
    reward.addEventListener('mouseout', () => setTimeout(fixRewardHeights, 450));
});

document.querySelectorAll('.delete-reward').forEach((i) => {
    i.onclick = () => {
        form = i.parentElement.children[0];
        if (confirm('Are you sure you want to delete this reward?'))
            form.submit();
    };
});

window.onload = fixGoalHeights;
window.onresize = fixGoalHeights;
window.onload = fixRewardHeights;
window.onresize = fixRewardHeights;