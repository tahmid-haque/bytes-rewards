"""
This file contains routes related to restaurant profiles.
"""

from flask import Blueprint, render_template
from flask_login import current_user, login_required
from modules.restaurant_profile_manager import RestaurantProfileManager

bp = Blueprint("profile", __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def view_profiles():
    """
    Allows users to view restaurant profiles that are set to public.
    """
    restaurant_profiles = RestaurantProfileManager("").get_public_profiles()
    return render_template('view_profiles.j2', profiles=restaurant_profiles)


@bp.route('/<string:obj_id>/board', methods=['GET', 'POST'])
@login_required
def view_board(obj_id):
    """
    Allows users to view the chosen restaurant's game board.
    """
    goals = []
    board_name = "Board is unavailable"
    rewards = []
    restaurant_users = RestaurantProfileManager("").get_public_users()
    for restaurant_user in restaurant_users:
        if str(restaurant_user["_id"]
              ) == obj_id and restaurant_user["profile"]["is_public"] is True:
            board_name = restaurant_user["bingo_board"]["name"]
            goal_ids = restaurant_user["bingo_board"]["board"] 
            custom_goals_dict = restaurant_user["goals"]
            for goal_id in goal_ids:
                for goal in current_user.get_goals():
                    if goal["_id"] == goal_id:
                        goals.append(goal["goal"])
                for goal in custom_goals_dict:
                    if goal["_id"] == goal_id:
                        goals.append(goal["goal"])
            reward_ids = restaurant_user["bingo_board"]["board_reward"]
            for reward_id in reward_ids:
                for reward in current_user.get_rewards():
                    if reward["_id"] == reward_id:
                        rewards.append(reward["reward"])
    return render_template('view_game_board.j2',
                           goals=goals,
                           name=board_name,
                           rewards=rewards)
