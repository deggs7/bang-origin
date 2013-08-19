# -*- coding: utf-8 -*-
"""
    shibeidao.views.bang
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Bang management and profile editing.

    :copyright: (c) 2013 by David De
"""
from flask import Module, redirect, url_for, request, \
    render_template, flash, session
from flask.ext.login import login_required
from flask.ext.login import current_user

from flask.ext.restless import ProcessingException

from .. import db
from .. import api_manager

from shibeidao.models.user import User
from shibeidao.models.bang import Bang
from shibeidao.forms.bang import CreateBangForm
from shibeidao.forms.bang import SearchBangForm
from shibeidao.forms.bang import SearchUserForm


bang = Module(__name__)


# Api management
def auth_func(**kwargs):
    if not current_user.is_authenticated():
        raise ProcessingException(message='Not authenticated', status_code=401)

def post_get_single(result=None, **kwargs):
    members = result.get('members',[])
    if not members:
        raise ProcessingException(message='Not authenticated', status_code=401)
    in_members = filter(lambda x:x.get('id')==current_user.id, members)
    if not in_members:
        raise ProcessingException(message='Not authenticated', status_code=401)

def pre_get_many(search_params=None, **kwargs):
    if search_params is None:
        return
    filt = dict(name='members__id',val=current_user.id,op='any')
    if 'filters' not in search_params:
        search_params['filters'] = []
    search_params['filters'].append(filt)

api_manager.create_api(Bang, methods=['GET', 'POST'],
                       preprocessors=dict(GET_SINGLE=[auth_func, ],
                                         GET_MANY=[auth_func, pre_get_many]),
                       postprocessors=dict(GET_SINGLE=[post_get_single])
                      )


@bang.route('/bang/', methods=['GET'])
@login_required
def bang_home():
    return render_template('bang/home.html', user=current_user)

@bang.route('/bang/add', methods=['GET', 'POST'])
@login_required
def add_bang():
    """
    """
    form = CreateBangForm(request.form)
    if request.method == 'POST':
    	if form.validate():
            # Create bang
            bang = Bang()
            bang.name = form.name.data
            bang.members.append(current_user)
            db.session.add(bang)
            return redirect(url_for('default.index'))
        else:
            flash("Can not create bang!")
            session['form'] = request.form
            return render_template('bang/add.html', form=form)
    else:
        return render_template('bang/add.html', form=form)

@bang.route('/bang/view/<bang_id>')
@login_required
def view_bang(bang_id):
    """
    """
    bang = Bang.query.filter_by(id=bang_id).first_or_404()
    return render_template('bang/view.html', bang=bang)

@bang.route('/bang/join/search', methods=['GET', 'POST'])
@login_required
def search_join():
    """
    """
    form = SearchBangForm(request.form)
    if request.method == 'POST':
        if form.validate():
            # Search
            bang_str = form.bang_str.data
            search_str = "%%%s%%" % bang_str
            bangs = Bang.query.filter(Bang.name.like(search_str)).all()
            return render_template('bang/search_join_result.html', bangs=bangs)
        else:
            flash('search words error!')
            session['form'] = form
            return redirect(url_for('bang.search_join'))
    else:
        return render_template('bang/search_join.html', form=form)


@bang.route('/bang/join/<bang_id>')
@login_required
def join_bang(bang_id):
    """
    """
    bang = Bang.query.filter_by(id=bang_id).first_or_404()
    try:
        if current_user not in bang.members:
            bang.members.append(current_user)
            db.session.add(bang)
            db.session.commit()
            flash('Joined successful!')
        else:
            flash('You already in this bang!')
    except:
        flash('Joined fail!')
    return redirect(url_for('default.index'))

@bang.route('/bang/invite/search/<bang_id>', methods=['GET', 'POST'])
@login_required
def search_invite(bang_id):
    """
    """
    form = SearchUserForm(request.form)
    if request.method == "POST":
        if form.validate():
            user_str = form.user_str.data
            search_str = '%%%s%%' % user_str
            users = User.query.filter(User.email.like(search_str)).all()
            return render_template('bang/search_invite_result.html',
                                   bang_id=bang_id, users=users)
        else:
            return redirect(url_for('bang.search_invite', bang_id=bang_id))
    else:
        return render_template('bang/search_invite.html', bang_id=bang_id, form=form)


@bang.route('/bang/invite/<bang_id>/<user_id>')
@login_required
def invite_user(bang_id, user_id):
    """
    """
    bang = Bang.query.filter_by(id=bang_id).first_or_404()
    user = User.query.filter_by(id=user_id).first_or_404()
    # todo: send email to user, wait for user submit. then add user to bang
    if user not in bang.members:
        bang.members.append(user)
        db.session.add(bang)
        db.session.commit()
        flash('user invite successful')
    else:
        flash('user already in this bang')
    return redirect(url_for('bang.view_bang', bang_id=bang.id))


