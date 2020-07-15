"""
This file contains routes related to cusomizing restaurant user's goals.
"""

from flask import Blueprint, render_template, request, redirect
from flask_login import current_user, login_required

bp = Blueprint("custom-goals", __name__)


@bp.route('/', methods=['POST', 'GET'])
@login_required
def view_custom_goals():
    """
    When retrieving this route, render a restaurant profile's list of
    customized goals.
    """
    if request.method == 'POST': # If POST request is received, add new custom goal
        goal = request.form["new_goal"]
        current_user.add_custom_goal(goal)
        return redirect("/custom-goals")
    else: # If GET request is received, render goal customization template
        custom_goals = current_user.get_custom_goals()
        return render_template('goal_customization.j2',
                               custom_goals=custom_goals)

@bp.route('/delete/<id>', methods=['POST'])
@login_required
def delete_custom_goal(goal_id):
    """
    When posting to this route, remove the goal given by goal_id.
    Redirect to the goal customization page on completion.
    """
    current_user.remove_custom_goal(goal_id)
    return redirect("/custom-goals")
