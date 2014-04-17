# -*- coding: utf-8 -*-
"""
bang_server.forms.bang
~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2013 by David De
"""
from flask.ext.wtf import Form, TextField, Required, BooleanField, \
        PasswordField, validators, ValidationError


class CreateBangForm(Form):
    name = TextField('Bang Name', [
        Required(),
        validators.Length(min=1, max=160),
    ])

class SearchBangForm(Form):
    bang_str = TextField('Bang keyword',[
        Required(),
        validators.Length(min=1, max=160),
    ])

class SearchUserForm(Form):
    user_str = TextField('User keyword',[
        Required(),
        validators.Length(min=1, max=100),
    ])

