from . import bp as database
from app import db
from flask import jsonify, request, url_for, render_template, redirect
import requests, re, random, itertools, math
from .models import Participant, Influencer, Trial, Gauntlet, Event

@database.route('/main', methods=['GET'])
def main():
    return render_template('database/main.html')

@database.route('/tests', methods=['GET'])
def tests():
    return render_template('database/tests.html')

@database.route('/populate', methods=['GET'])
def populate_database():
    return render_template('database/populate.html')

# Create New for Production
# New event
@database.route('/new_event', methods=['GET', 'POST'])
def new_event():
    return render_template('database/new_event.html')

# New gauntlet
@database.route('/new_gauntlet', methods=['GET', 'POST'])
def new_gauntlet():
    return render_template('database/new_gauntlet.html')

# New trial
@database.route('/new_trial', methods=['GET', 'POST'])
def new_trial():
    return render_template('database/new_trial.html')

# New participant
@database.route('/new_participant', methods=['GET', 'POST'])
def new_participant():
    return render_template('database/new_participant.html')

# New influencer
@database.route('/new_influencer', methods=['GET', 'POST'])
def new_influencer():
    return render_template('database/new_influencer.html')

# New obstacle
@database.route('/new_obstacle', methods=['GET', 'POST'])
def new_obstacle():
    return render_template('database/new_obstacle.html')


# Test Cases for Development
# test event
@database.route('/test_event', methods=['GET', 'POST'])
def test_event():
    return render_template('database/test_event.html')

# test gauntlet
@database.route('/test_gauntlet', methods=['GET', 'POST'])
def test_gauntlet():
    return render_template('database/test_gauntlet.html')

# test trial
@database.route('/test_trial', methods=['GET', 'POST'])
def test_trial():
    return render_template('database/test_trial.html')

# test participant
@database.route('/test_participant', methods=['GET', 'POST'])
def test_participant():
    return render_template('database/test_participant.html')

# test influencer
@database.route('/test_influencer', methods=['GET', 'POST'])
def test_influencer():
    return render_template('database/test_influencer.html')

# test obstacle
@database.route('/test_obstacle', methods=['GET', 'POST'])
def test_obstacle():
    return render_template('database/test_obstacle.html')



# Population for New Database

# Random Population Button
@database.route('/arbitrary', gethods=['GET', 'POST'])
def arbitrary():
    return redirect(url_for('database.main'))


# populate event
@database.route('/populate_event', methods=['GET', 'POST'])
def populate_event():
    # Create 100 events
    count = 0
    while count < 100:
        # Create a new Event
        new_event = Event()
        event_data = {
            'name': f'Event_{count}',
            'description': f'Event_Description_{count}'
        }
        new_event.set_attributes(event_data)
        new_event.save_item()

        # Select the event from the database
        this_event = Event.query.filter_by(name=f'Event_{count}').first()

        # Select a random Influencer
        influencer_number = random.randint(0, 19999)
        this_influencer = Influencer.query.filter_by(name_1=f'Influencer_{influencer_number}').first()
        # Associate an Influencer with the event
        this_event.influencers.append(this_influencer)
        db.session.commit()

        # Select 100 random participants
        participant_count = 0
        while participant_count < 100:
            participant_number = random.randint(0, 9999)
            this_participant = Participant.query.filter_by(name_1=f'First {participant_number}').first()
            participant_count += 1

            # Associate the Participants with the Event
            this_event.participants.append(this_participant)
            db.session.commit()

        count += 1

    return redirect(url_for('database.main'))

# populate gauntlet
@database.route('/populate_gauntlet', methods=['GET', 'POST'])
def populate_gauntlet():
    # Create 100 Gauntlets
    count = 0
    while count < 100:
        # Create random assortment of 10 trials
        trials_list = []
        trials_chosen = 0
        while trials_chosen < 10:
            random_id = random.randint(1, 100)
            trials_list.append(Trial.query.get(random_id))
            trials_chosen += 1
        # print(trials_list)
        
        # Sum the duration of all trials
        trials_duration = 0
        for trial in trials_list:
            trials_duration += trial.duration
        trial_days = trials_duration/28800
        trial_weeks = trial_days/5
        minimum_weekends = math.floor(trial_weeks)
        minimum_days = trial_days + (minimum_weekends*2)
        
        extra_days = random.randint(0, 10)

        all_class_days = minimum_days + extra_days
        all_weekends = (all_class_days/5)
        total_days = math.ceil(all_class_days) + math.floor(all_weekends)

        # Create a new gauntlet
        new_gauntlet = Gauntlet()
        byte_names = requests.get('https://random-word-api.herokuapp.com/word?number=2')
        decoded_names = byte_names.content.decode('utf-8')
        fake_names = re.findall(r'"(\w+)"', decoded_names)
        gauntlet_data = {
            'name': fake_names[0],
            'description':fake_names[1],
            'duration': int(total_days*28800)
        }
        new_gauntlet.set_attributes(gauntlet_data)
        new_gauntlet.save_item()

        # Append trials to the gauntlet
        this_gauntlet = Gauntlet.query.filter_by(name=fake_names[0]).first()
        for trial in trials_list:
            this_gauntlet.trials.append(trial)
            db.session.commit()
        count += 1

    return redirect(url_for('database.main'))

# populate trial
@database.route('/populate_trial', methods=['GET', 'POST'])
def populate_trial():
    count = 0
    difficulty_range = list(range(1, 11))
    duration_range = list(range(1,11))
    stat_range = [difficulty_range, duration_range]
    possible_trials = list(itertools.product(*stat_range))
    for trial in possible_trials:
        new_trial = Trial()
        trial_data = {
            'name':f'Trial_{count}',
            'description':f'Description_{count}',
            'difficulty':trial[0],
            'duration':trial[1]*28800
        }
        count+=1
        new_trial.set_attributes(trial_data)
        new_trial.save_item()
    return redirect(url_for('database.main'))

# populate participant
@database.route('/populate_participant', methods=['GET', 'POST'])
def populate_participant():
    int_range = list(range(1,11))
    end_range = list(range(1,11))
    vol_range = list(range(1,11))
    back_range = list(range(1,11))
    stat_range = [int_range, end_range, vol_range, back_range]
    possible_participants = list(itertools.product(*stat_range))
    count = 0
    for student in possible_participants:
        new_participant = Participant()
        participant_data = {
            'name_1':f'First {count}',
            'name_2':f'Last {count}',
            'attribute_1': student[0],
            'attribute_2': student[1],
            'attribute_3': student[2],
            'attribute_4': student[3] * 28800,
            'attribute_5': student[3] * 28800
        }
        count += 1
        new_participant.set_attributes(participant_data)
        new_participant.save_item()

    return redirect(url_for('database.main'))

# populate influencer
@database.route('/populate_influencer', methods=['GET', 'POST'])
def populate_influencer():
    quality_range = list(range(1,11)) # instructor quality
    commitment_range = list(range(1,11)) # time spent outside of class
    volatility_range = list(range(1,11)) # vulnerability to obstacles
    concentration_range = list(range(1,11)) # time spent off-topic
    availability_range = [0, 1] # weekend availability (2 hr / day)
    stat_range = [quality_range, commitment_range, volatility_range, concentration_range, availability_range]
    possible_influencers = list(itertools.product(*stat_range))
    count = 0
    for instructor in possible_influencers:
        new_influencer = Influencer()
        participant_data = {
            'name_1':f'Influencer_{count}',
            'name_2':f'Influencer_{count}',
            'attribute_1': instructor[0],
            'attribute_2': instructor[1],
            'attribute_3': instructor[2],
            'attribute_4': instructor[3],
            'attribute_5': instructor[4]
        }
        count += 1
        new_influencer.set_attributes(participant_data)
        new_influencer.save_item()

    return redirect(url_for('database.main'))

# populate obstacle
@database.route('/populate_obstacle', methods=['GET', 'POST'])
def populate_obstacle():
    return render_template('database/populate_obstacle.html')