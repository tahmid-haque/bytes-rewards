"""
This file contains routes related to customer profiles.
"""

from flask import Blueprint, render_template
from flask_login import current_user, login_required

bp = Blueprint("customer", __name__)


@bp.route('/rewards')
@login_required
def show_rewards():
    """
    Shows the user their reward progress for all restaurants.
    """
    active_rewards, redeemed_rewards = current_user.get_reward_progress()
    return render_template('rewards.j2',
                           active_rewards=active_rewards,
                           redeemed_rewards=redeemed_rewards)
