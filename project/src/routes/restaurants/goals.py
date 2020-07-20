"""
This file contains routes related to cusomizing restaurant user's goals.
"""

from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_required

bp = Blueprint("goals", __name__)


@bp.route('/')
@login_required
def view_custom_goals():
    """
    When retrieving this route, render a restaurant profile's list of
    customized goals.
    Prerequisite: User is logged in.
    """
    goals = current_user.get_custom_goals()
    return render_template('customization.j2', goals=goals)

@bp.route('/add', methods=['POST'])
@login_required
def add_goal():
    """
    When posting to this route, add the goal given in form.
    Redirect to the goal customization page on completion.
    Prerequisite: User is logged in.
    """
    goal = request.form["goal"]
    added = current_user.add_custom_goal(goal)
    if not added:
        flash("This is a duplicate goal. Goal not added.")
    return redirect("/goals")

@bp.route('/delete', methods=['POST'])
@login_required
def delete_goal():
    """
    When retrieving this route, delete the goal given by goal_id.
    Redirect to the goal customization page on completion.
    Prerequisite: User is logged in.
    """
    goal_id = request.form["deleted-goal"]
    removed = current_user.remove_custom_goal(goal_id)
    if not removed:
        flash("This goal in on your current game board; replace and try again")
    return redirect("/goals")
