# -*- coding: utf-8 -*-
"""
    bang_server.models.bang
    ~~~~~~~~~~~~~~~~~~~~

    Bang and Activity base objects. To be subclassed by separate bang
    types.

    :copyright: (c) 2013 by David De
"""


from .. import db

# many-to-many relation between Bang & User
bangs_members = db.Table('bangs_members',
        db.Column('bang_id', db.Integer, db.ForeignKey('bang.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
        )

class Bang(db.Model):
    """
    one bang has some members and some activities
    """
    __tablename__ = 'bang'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(160))
    # level = db.Column(db.Integer(1))

    activities = db.relationship('Activity', backref=db.backref('bang'))

    # members
    members = db.relationship('User', secondary=bangs_members, backref=db.backref('bangs'))

    def get_id(self):
        return self.id

    def __init__(self):
        pass

    def __repr__(self):
        return '<User %r>' % self.email

# many-to-many relation between Activity & User
activities_invitees = db.Table('activities_invitees',
        db.Column('activity_id', db.Integer, db.ForeignKey('activity.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        )

class Activity(db.Model):
    """
    many activities belong one bang
    one activity has some participants from one bang
    """
    __tablename__ = "activity"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(160))
    crontab = db.Column(db.String(20))

    # bang
    bang_id = db.Column(db.Integer, db.ForeignKey('bang.id'))

    # invitees of this activity
    invitees = db.relationship('User', secondary=activities_invitees, backref=db.backref('activities'))

    # creater

    # create time

    # records
    activityrecords = db.relationship('ActivityRecord', backref=db.backref('activity'))



activityrecords_participants = db.Table('activityrecords_participants',
        db.Column('activityrecord_id', db.Integer, db.ForeignKey('activityrecord.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        )

class ActivityRecord(db.Model):
    """
    """
    __tablename__ = "activityrecord"
    id = db.Column('id', db.Integer, primary_key=True)

    # activity
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))

    # participant
    participants = db.relationship('User', secondary=activityrecords_participants, backref=db.backref('activityrecords'))

