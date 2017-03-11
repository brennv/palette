# -*- coding: utf-8 -*-
"""Blog section."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

# from flask_security import login_required, login_user, logout_user
from flask_login import login_required, login_user, logout_user

from generic.extensions import login_manager
from generic.public.forms import LoginForm
# from generic.user.forms import RegisterForm
from generic.user.models import User
from generic.utils import flash_errors

blueprint = Blueprint('blog', __name__, static_folder='../static')


@blueprint.route('/blog/')
def blog():
    """Blog page."""
    form = LoginForm(request.form)
    return render_template('blog/blog.html', form=form)


@blueprint.route('/blog/post/1')
def post1():
    """Blog post page."""
    form = LoginForm(request.form)
    return render_template('blog/blog-post-1.html', form=form)


@blueprint.route('/blog/post/2')
def post2():
    """Blog post page."""
    form = LoginForm(request.form)
    return render_template('blog/blog-post-2.html', form=form)


@blueprint.route('/blog/post/3')
def post3():
    """Blog post page."""
    form = LoginForm(request.form)
    return render_template('blog/blog-post-3.html', form=form)
