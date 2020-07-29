"""
This file contains routes related to customizing restaurant user's goals.
"""

from flask import Blueprint, render_template, request, redirect, flash, jsonify
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

@bp.route('/verify-goal/<string:code_data>', methods=['POST', 'GET'])
@login_required
def verify_goal(code_data):
    """

    """
    data = code_data.split("+")
    goals = current_user.get_goals()
    goal = ""
    for goal in goals:
        if str(goal['_id']) == data[1]:
            return jsonify({'goal': goal['goal']})

    return jsonify({'goal': "No Goal Found"})


@bp.route('/finish-goal', methods=['POST', 'GET'])
@login_required
def finished_goal():
    data = request.form["code"].split("+")
    if len(data) != 3:
        flash("Invalid QR code!")
        return redirect("/profile/qr-verification")
    user = data[0]
    goal_id = data[1]
    position = data[2]
    msg = "Successfully marked as completed!"
    msg = current_user.complete_goal(user, goal_id, position)
    flash(msg)
    return redirect("/profile/qr-verification")

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
