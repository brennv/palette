# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required
# from flask_security import login_required


blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """List members."""
    return render_template('users/members.html')

@blueprint.route('/reservation/')
@login_required
def reservation():
    """Reservation page."""
    # form = LoginForm(request.form)
    return render_template('users/reservation.html')  # , form=form)
