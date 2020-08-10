"""
This file contains routes related to customer profiles.
"""

from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_required
from modules.owner.restaurant_profile_manager import RestaurantProfileManager
from modules.owner.game_board import GameBoardManager
from modules.owner.public_profile import PublicProfileModifier
from modules.customer.favourite import get_favourite
from modules.customer.customer_board import set_board_progress, reset_complete_board

bp = Blueprint("restaurants", __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def view_profiles():
    """
    Allows users to view restaurant profiles that are set to public.
    """
    rpm = RestaurantProfileManager("")
    restaurant_profiles = PublicProfileModifier(rpm).get_public_profiles()
    favourite = get_favourite(current_user)
    return render_template('view_profiles.j2',
                           profiles=restaurant_profiles,
                           favourite=favourite)


@bp.route('/<string:obj_id>/board', methods=['GET', 'POST'])
@login_required
def view_board(obj_id):
    """
    Allows users to view the chosen restaurant's game board.
    """
    username = current_user.get_id()
    rpm = RestaurantProfileManager("")
    gpm = GameBoardManager(rpm)
    gpm.update_board(obj_id)
    board = gpm.get_restaurant_board_by_id(obj_id)
    set_board_progress(current_user, board, obj_id)
    board["expiry_date"] = board["expiry_date"].strftime(
        "%B X%d, %Y - X%I:%M %p UTC").replace("X0", "X").replace("X", "")

    return render_template('view_game_board.j2',
                           goals=board["board"],
                           name=board["name"],
                           rewards=board["board_reward"],
                           cust_id=username,
                           size=board["size"],
                           date=board["expiry_date"])


@bp.route('/<string:obj_id>/reset-board', methods=['GET', 'POST'])
@login_required
def reset_board(obj_id):
    """
    When posting to this route, reset the bingo board goals.
    Redirect to the bingo board on completion.
    """
    reset_complete_board(current_user, obj_id)
    return redirect("board")


@bp.route('/<string:prof_id>/profile', methods=['GET', 'POST'])
@login_required
def view_restaurant_profile(prof_id):
    """
    Allows users to view the chosen restaurant's profile.
    """
    rpm = RestaurantProfileManager("")
    rest_info = PublicProfileModifier(rpm).get_restaurant_profile_by_id(prof_id)
    return render_template('view_profile.j2',
                           restaurant_name=rest_info["name"],
                           address=rest_info["location"]["address"],
                           city=rest_info["location"]["city"],
                           province=rest_info["location"]["province"],
                           postal_code=rest_info["location"]["postal_code"],
                           phone_number=rest_info["phone_number"],
                           category=rest_info["category"],
                           rest_img=rest_info["image"],
                           description=rest_info["description"])
