# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment

css = Bundle(
    'libs/bootstrap/dist/css/bootstrap.css',
    # 'libs/font-awesome/css/font-awesome.css',  # doesn't pull fonts
    'css/style.css',
    'css/footer.css',
    'css/layout.css',
    'css/nav.css',
    filters='cssmin',
    output='public/bundle/common.css'
)

js = Bundle(
    'libs/jquery/dist/jquery.js',
    'libs/bootstrap/dist/js/bootstrap.js',
    'libs/bootstrap-growl/jquery.bootstrap-growl.js',
    'js/plugins.js',
    filters='jsmin',
    output='public/bundle/common.js'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
