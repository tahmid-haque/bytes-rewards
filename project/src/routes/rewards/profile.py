"""
This file contains routes related to customer profiles.
"""

from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_required
from modules.owner.restaurant_profile_manager import RestaurantProfileManager
from modules.owner.public_profile import PublicProfileModifier
from modules.customer.favourite import update_favourite, get_favourite, get_favourite_doc
from modules.customer.customer_board import get_reward_progress

bp = Blueprint("profile", __name__)


@bp.route('/favourites/<string:obj_id>/update', methods=['GET', 'POST'])
@login_required
def favourite_restaurant(obj_id):
    """
    Allows users to add and remove restaurants from "favourite"
    """
    update_favourite(current_user, obj_id)
    return redirect("/")


@bp.route('/favourites', methods=['GET', 'POST'])
@login_required
def view_favourites():
    """
    Allows users to view restaurants from "favourite"
    """
    favourite = get_favourite(current_user)
    rpm = RestaurantProfileManager("")
    profiles = PublicProfileModifier(rpm).get_public_profiles()
    list_fav = get_favourite_doc(profiles, favourite)
    return render_template('view_favourites.j2',
                           profiles=list_fav,
                           favourite=favourite)


@bp.route('/favourites/<string:obj_id>/favourite', methods=['GET', 'POST'])
@login_required
def view_favourite_restaurant(obj_id):
    """
    Allows users to remove restaurants from "favourite" while on "favourites" page
    """
    update_favourite(current_user, obj_id)
    return redirect('/personal/favourites')


@bp.route('/rewards')
@login_required
def show_rewards():
    """
    Shows the user their reward progress for all restaurants.
    """
    active_rewards, redeemed_rewards = get_reward_progress(current_user)
    return render_template('rewards.j2',
                           active_rewards=active_rewards,
                           redeemed_rewards=redeemed_rewards)
