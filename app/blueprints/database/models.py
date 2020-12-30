from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField

# Database Tables

# Association Tables
participant_event = db.Table('participant_event',
    db.Column('participant_id', db.Integer, db.ForeignKey('participant.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

influencer_event = db.Table('influencer_event',
    db.Column('influencer_id', db.Integer, db.ForeignKey('influencer.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

obstacle_event = db.Table('obstacle_event',
    db.Column('obstacle_id', db.Integer, db.ForeignKey('obstacle.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

gauntlet_event = db.Table('gauntlet_event',
    db.Column('gauntlet_id', db.Integer, db.ForeignKey('gauntlet.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

trial_gauntlet = db.Table('trial_gauntlet',
    db.Column('trial_id', db.Integer, db.ForeignKey('trial.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

# Main Tables

# Event = Collection of all necessary information for a test
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_type = db.Column(db.String(50), default='Event')
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    gauntlets = db.relationship('Gauntlet', secondary=participant_event, backref=db.backref('events', lazy='dynamic')) # Gauntlets in association table
    participants = db.relationship('Participant', secondary=participant_event, backref=db.backref('events', lazy='dynamic')) # Participants in association table
    influencers = db.relationship('Influencer', secondary=influencer_event, backref=db.backref('events', lazy='dynamic')) # Influencers in association table
    obstacles = db.relationship('Obstacle', secondary=obstacle_event, backref=db.backref('events', lazy='dynamic')) # Obstacles in association table

    def __repr__(self):
        return f'<Event | ID: {self.id}> | Name: {self.name} >'
    
    def set_attributes(self, data_dict):
        for attribute in ['name', 'gauntlet', 'description']:
            if attribute in data_dict:
                setattr(self, attribute, data_dict[attribute])

    # WIP
    def to_dict(self):
        attributes = {
            'id':self.id,
            'name':self.name,
            'description': self.description,
            'gauntlet_ID':self.gauntlet,
            # 'participants':self.participants,
            # 'influencers':self.influencers,
            # 'obstacles':self.obstacles
        }
        return attributes

    def save_item(self):
        db.session.add(self)
        db.session.commit()

    def remove_item(self):
        db.session.delete(self)
        db.session.commit()

    def update_item(self):
        db.session.commit()

# Gauntlet = A collection of Trials
class Gauntlet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_type = db.Column(db.String(50), default='Gauntlet')
    name = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    description = db.Column(db.String(500))
    trials = db.relationship('Trial', secondary=trial_gauntlet, backref=db.backref('gauntlets', lazy='dynamic'))
    events = db.relationship('Event', secondary=gauntlet_event, backref=db.backref('gauntlets', lazy='dynamic'))

    def __repr__(self):
        return f'<Gauntlet | ID: {self.id}> | Name: {self.name} >'
    
    def set_attributes(self, data_dict):
        for attribute in ['name', 'duration', 'description']:
            if attribute in data_dict:
                setattr(self, attribute, data_dict[attribute])

    # WIP
    def to_dict(self):
        attributes = {
            'name' : self.name,
            'duration': self.duration,
            'description': self.description,
            # 'trials':self.trials,
            # 'events':self.events
        }
        return attributes

    def save_item(self):
        db.session.add(self)
        db.session.commit()

    def remove_item(self):
        db.session.delete(self)
        db.session.commit()

    def update_item(self):
        db.session.commit()

# Trial = A test all participants take part in
class Trial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_type = db.Column(db.String(50), default='Trial')
    name = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    description = db.Column(db.String(500))
    gauntlets = db.relationship('Gauntlet', secondary=trial_gauntlet, backref=db.backref('trials', lazy='dynamic'))

    def __repr__(self):
        return f'<Trial | ID: {self.id}> | Name: {self.name} >'
    
    def set_attributes(self, data_dict):
        for attribute in ['name', 'duration', 'difficulty', 'description']:
            if attribute in data_dict:
                setattr(self, attribute, data_dict[attribute])

    def to_dict(self):
        attributes = {
            'id' : self.id,
            'name': self.name,
            'duration' : self.duration,
            'dificulty' : self.difficulty,
            'description' : self.description,
            # 'gauntlets' : self.gauntlets
        }
        return attributes

    def save_item(self):
        db.session.add(self)
        db.session.commit()

    def remove_item(self):
        db.session.delete(self)
        db.session.commit()

    def update_item(self):
        db.session.commit()

# Participant = An object which will be tested via the gauntlet
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_1 = db.Column(db.String(50), default='Name_1')
    name_2 = db.Column(db.String(50), default='Name_2')
    attribute_1 = db.Column(db.Integer)
    attribute_2 = db.Column(db.Integer)
    attribute_3 = db.Column(db.Integer)
    attribute_4 = db.Column(db.Integer)
    attribute_5 = db.Column(db.Integer)
    events = db.relationship('Event', secondary=participant_event, backref=db.backref('participants', lazy='dynamic'))

    def __repr__(self):
        return f'<Participant | ID: {self.id}> | Name: {self.name_1} {self.name_2} >'
    
    def set_attributes(self, data_dict):
        for attribute in [ 'name_1', 'name_2', 'attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'attribute_5' ]:
            if attribute in data_dict:
                setattr(self, attribute, data_dict[attribute])

    # WIP
    def to_dict(self):
        attributes = {
            'name_1' : self.name_1,
            'name_2' : self.name_2,
            'attribute_1' : self.attribute_1,
            'attribute_2' : self.attribute_2,
            'attribute_3' : self.attribute_3,
            'attribute_4' : self.attribute_4,
            'attribute_5' : self.attribute_5,
            # 'events' : self.events
        }
        return attributes

    def save_item(self):
        db.session.add(self)
        db.session.commit()

    def remove_item(self):
        db.session.delete(self)
        db.session.commit()

    def update_item(self):
        db.session.commit()

# Influencer = An object which affects all participants
class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_type = db.Column(db.String(50), default='Influencer')
    name_1 = db.Column(db.String(50), default='Name_1')
    name_2 = db.Column(db.String(50), default='Name_2')
    attribute_1 = db.Column(db.Integer)
    attribute_2 = db.Column(db.Integer)
    attribute_3 = db.Column(db.Integer)
    attribute_4 = db.Column(db.Integer)
    attribute_5 = db.Column(db.Integer)
    events = db.relationship('Event', secondary=influencer_event, backref=db.backref('influencers', lazy='dynamic'))

    def __repr__(self):
        return f'<Influencer | ID: {self.id}> | Name: {self.name_1} {self.name_2} >'
    
    def set_attributes(self, data_dict):
        for attribute in [ 'name_1', 'name_2', 'attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'attribute_5' ]:
            if attribute in data_dict:
                setattr(self, attribute, data_dict[attribute])

    # WIP
    def to_dict(self):
        attributes = {
            'name_1' : self.name_1,
            'name_2' : self.name_2,
            'attribute_1' : self.attribute_1,
            'attribute_2' : self.attribute_2,
            'attribute_3' : self.attribute_3,
            'attribute_4' : self.attribute_4,
            'attribute_5' : self.attribute_5,
            # 'events': self.events
        }
        return attributes

    def save_item(self):
        db.session.add(self)
        db.session.commit()

    def remove_item(self):
        db.session.delete(self)
        db.session.commit()

    def update_item(self):
        db.session.commit()

# Obstacle = A temporary effect for an individual participant
class Obstacle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_type = db.Column(db.String(50), default='Obstacle')
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    duration = db.Column(db.Integer)
    intensity = db.Column(db.Integer) # 1-100, decribes how much the event affects the participant
    chance = db.Column(db.Integer) # Chance of event triggering per tick
    events = db.relationship('Event', secondary=obstacle_event, backref=db.backref('obstacles', lazy='dynamic'))

    def __repr__(self):
        return f'<Obstacle | ID: {self.id}> | Name: {self.name} >'
    
    def set_attributes(self, data_dict):
        for attribute in ['name', 'description', 'duration', 'intensity', 'chance']:
            if attribute in data_dict:
                setattr(self, attribute, data_dict[attribute])

    def to_dict(self):
        attributes = {
            'name' : self.name,
            'description' : self.description,
            'duration' : self.duration,
            'intensity' : self.intensity,
            'chance' : self.chance,
            # 'events' : self.events
        }
        return attributes

    def save_item(self):
        db.session.add(self)
        db.session.commit()

    def remove_item(self):
        db.session.delete(self)
        db.session.commit()

    def update_item(self):
        db.session.commit()
