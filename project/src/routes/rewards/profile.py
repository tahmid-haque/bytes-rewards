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
    username = current_user.get_id()
    rpm = RestaurantProfileManager("")
    board = rpm.get_restaurant_board_by_id(obj_id)
    current_user.set_board_progress(board, obj_id)

    return render_template('view_game_board.j2',
                           goals=board["board"],
                           name=board["name"],
                           rewards=board["board_reward"],
                           cust_id=username)
