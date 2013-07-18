# -*- coding: utf-8 -*-
"""
    shibeidao
    ~~~~~~~~

    This is a new Flask shibeidao for a basic Flask-driven site with user auth,
    signup, e-mailing, and password recovery. Customize to fit your needs and
    go.

    :copyright: (c) 2012 by Jeff Long
"""
import os
from flask import Flask, render_template, request_started, g

# Extensions
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from sqlalchemy.orm import exc as orm_exc
from flask.ext.bootstrap import Bootstrap
from flask.ext.restless import APIManager


# App setup
app = Flask(__name__)
app.config.from_object('shibeidao.config.DevelopmentConfig')
db = SQLAlchemy(app)

# Api management
api_manager = APIManager(app, flask_sqlalchemy_db=db)

# bootstrap
Bootstrap(app)
app.config['BOOTSTRAP_USE_MINIFIED'] = True
app.config['BOOTSTRAP_USE_CDN'] = True
app.config['BOOTSTRAP_FONTAWESOME'] = True
app.config['SECRET_KEY'] = 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

# Login management
login_manager = LoginManager()
login_manager.login_view = "default.index"
login_manager.login_message = u"You must log in to access this page."
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    from models.user import User
    try:
        user = User.query.filter(User.id == userid).one()
    except orm_exc.NoResultFound:
        user = None
    return user


# HTTP error handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

# Load views
from .views.session import user_session
from .views.default import default
from .views.account import account
from .views.bang import bang

# Register views
app.register_module(default)
app.register_module(user_session)
app.register_module(account)
app.register_module(bang)

# Additional setup
import hooks
import context_processors

'''
Development environment setup
Enables logging and fixes serving static files from the dev server
(runserver.py).
'''
if app.config['DEBUG']:
    import logging
    working_dir = os.path.dirname(os.path.abspath(__file__))
    file_handler = logging.FileHandler('%s/logs/app.log' % working_dir)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

    def setup_static(sender):
        '''Setup static file serving in dev environment'''
        from werkzeug import SharedDataMiddleware
        import os
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/': os.path.join(os.path.dirname(__file__), 'static')
        })
    request_started.connect(setup_static, app)
