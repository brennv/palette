# -*- coding: utf-8 -*-
"""Shop section, including search and posting items."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

# from flask_security import login_required, login_user, logout_user
from flask_login import login_required, login_user, logout_user

from palette.extensions import login_manager
from palette.public.forms import LoginForm
# from palette.user.models import User
from palette.utils import flash_errors

blueprint = Blueprint('shop', __name__, static_folder='../static')


@blueprint.route('/find/')
def find():
    """Find item."""
    form = LoginForm(request.form)
    return render_template('shop/find.html', form=form)


@blueprint.route('/item/')
def item():
    """item page."""
    form = LoginForm(request.form)
    return render_template('shop/item.html', form=form)
