# -*- coding: utf-8 -*-
"""
    shibeidao.config
    ~~~~~~~~~~~~~~~

    Flask shibeidao basic configuration file for different setups.

    :copyright: (c) 2012 by Jeff Long
"""
import os


class Config(object):
    # Site meta
    SITE_TITLE = 'ShiBeiDao'
    SITE_DESCRIPTION = 'A site for your live.'

    DEBUG = True
    TESTING = True
    ADMINS = frozenset(['admin@shibeidao.com'])
    SECRET_KEY = 'YOUR-CRAZY-AWESOME-SECRET-SAUCE'
    SALT = 'YOUR-SUPER-SALTY-POTATO-CHIPS'

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = 'YOUR-NEAT-SESSION-KEY'

    # Flask-SQLAlchemy setup, default to sqlite in-memory database
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

    # Flask-Mail setup
    MAIL_DEBUG = True
    MAIL_FAIL_SILENTLY = False


class ProductionConfig(Config):
    TESTING = False
    DEBUG = False

    # Flask-SQLAlchemy setup
    SQLALCHEMY_DATABASE_URI = 'mysql://youruser:yourpass@localhost/database'
    SQLALCHEMY_POOL_RECYCLE = 10


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

    # Flask-SQLAlchemy setup
    # SQLALCHEMY_DATABASE_URI = 'mysql://youruser:yourpass@localhost/database'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.db'
    SQLALCHEMY_ECHO = True

    # Flask-Mail setup
    '''If you want to use gmail to test your e-mailing, just enter
    smtp.gmail.com for the server and then your e-mail/password and
    change the MAIL_DEFAULT_SENDER as yourself as well.'''
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'do-not-reply@shibeidao.com'
    MAIL_PASSWORD = '5iteam'
    MAIL_DEBUG = True
    MAIL_FAIL_SILENTLY = True
    MAIL_DEFAULT_SENDER ='do-not-reply@shibeidao.com'


class TestingConfig(Config):
    CSRF_ENABLED = False
    TESTING = True
