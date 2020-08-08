"""
This file contains routes related to customizing restaurant user's goals and rewards.
"""

from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_required

bp = Blueprint("customize", __name__)


@bp.route('/')
@login_required
def view_customize():
    """
    When retrieving this route, render a restaurant profile's list of
    customized goals and rewards.
    Prerequisite: User is logged in.
    """
    goals = current_user.get_custom_goals()
    rewards = current_user.get_custom_rewards()
    return render_template('customization.j2', goals=goals, rewards=rewards)


@bp.route('/add-goal', methods=['POST'])
@login_required
def add_goal():
    """
    When posting to this route, add the goal given in form.
    Redirect to the customization page on completion.
    Prerequisite: User is logged in.
    """
    goal = request.form["goal"]
    added = current_user.add_custom_goal(goal)
    if not added:
        flash("This is a duplicate goal. Goal not added.")
    return redirect("/customize")


@bp.route('/delete-goal', methods=['POST'])
@login_required
def delete_goal():
    """
    When retrieving this route, delete the goal given by goal_id.
    Redirect to the customization page on completion.
    Prerequisite: User is logged in.
    """
    goal_id = request.form["deleted-goal"]
    removed = current_user.remove_custom_goal(goal_id)
    if removed == "current":
        flash("This goal in on your current game board; cannot be deleted")
    elif removed == "future":
        flash("This goal in on your future game board; replace and try again")
    return redirect("/customize")


@bp.route('/add-reward', methods=['POST'])
@login_required
def add_reward():
    """
    When posting to this route, add the reward given in form.
    Redirect to the customization page on completion.
    Prerequisite: User is logged in.
    """
    reward = request.form["reward"]
    added = current_user.add_custom_reward(reward)
    if not added:
        flash("This is a duplicate reward. Reward not added.")
    return redirect("/customize")


@bp.route('/delete-reward', methods=['POST'])
@login_required
def delete_reward():
    """
    When retrieving this route, delete the reward given by reward_id.
    Redirect to the customization page on completion.
    Prerequisite: User is logged in.
    """
    reward_id = request.form["deleted-reward"]
    removed = current_user.remove_custom_reward(reward_id)
    if removed == "current":
        flash("This reward in on your current game board; cannot be deleted")
    elif removed == "future":
        flash("This reward in on your future game board; replace and try again")
    return redirect("/customize")
