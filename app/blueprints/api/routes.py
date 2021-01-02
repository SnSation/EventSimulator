from . import bp as api
from app import db
from flask import jsonify, request, url_for, render_template, redirect
import requests, re, random, math
from app.blueprints.database.models import Participant, Influencer, Trial, Gauntlet, Event
from .models import ChooseEvent

@api.route('/main', methods=['GET'])
def main():
    choose_event = ChooseEvent()
    if choose_event.validate_on_submit():
        return redirect(url_for('api.single_event/'+ choose_event.idno.data))

    context = {
        'choose_event' : choose_event
    }

    return render_template('api/main.html', **context)

@api.route('/all_events', methods=['GET'])
def all_events():
    all_events = [event.to_dict() for event in Event.query.all()]
    for event in all_events:
        # Make Gauntlets Jsonifiable
        gauntlet_list = []
        for gauntlet in event['gauntlets']:
            gauntlet_dict = gauntlet.to_dict()

            # Make Trials Jsonifiable
            trial_list = []
            for trial in gauntlet_dict['trials']:
                trial_dict = trial.to_dict()
                trial_list.append(trial_dict)
            gauntlet_dict['trials'] = trial_list

            gauntlet_list.append(gauntlet_dict)

        event['gauntlets'] = gauntlet_list

        # Make Participants Jsonifiable
        participant_list = []
        for participant in event['participants']:
            participant_dict = participant.to_dict()
            participant_list.append(participant_dict)
        event['participants'] = participant_list

        # Make Influencers Jsonifiable
        influencer_list = []
        for influencer in event['influencers']:
            influencer_dict = influencer.to_dict()
            influencer_list.append(influencer_dict)
        event['influencers'] = influencer_list

    return jsonify(all_events)

@api.route('/single_event/<idno>', methods=['GET'])
def single_event(idno):
    event = Event.query.filter_by(id=idno).first().to_dict()

    # Make Gauntlets Jsonifiable
    gauntlet_list = []
    for gauntlet in event['gauntlets']:
        gauntlet_dict = gauntlet.to_dict()

        # Make Trials Jsonifiable
        trial_list = []
        for trial in gauntlet_dict['trials']:
            trial_dict = trial.to_dict()
            trial_list.append(trial_dict)
        gauntlet_dict['trials'] = trial_list

        gauntlet_list.append(gauntlet_dict)

    event['gauntlets'] = gauntlet_list

    # Make Participants Jsonifiable
    participant_list = []
    for participant in event['participants']:
        participant_dict = participant.to_dict()
        participant_list.append(participant_dict)
    event['participants'] = participant_list

    # Make Influencers Jsonifiable
    influencer_list = []
    for influencer in event['influencers']:
        influencer_dict = influencer.to_dict()
        influencer_list.append(influencer_dict)
    event['influencers'] = influencer_list

    return jsonify(event)

@api.route('/all_participants', methods=['GET'])
def all_participants():
    participants = [participant.to_dict() for participant in Participant.query.all()]

    return jsonify(participants)

@api.route('/all_influencers', methods=['GET'])
def all_influencers():
    influencers = [influencer.to_dict() for influencer in Influencer.query.all()]

    return jsonify(influencers)

@api.route('/all_trials', methods=['GET'])
def all_gauntlets():
    trials = [trial.to_dict() for trial in Trial.query.all()]

    return jsonify(trials)