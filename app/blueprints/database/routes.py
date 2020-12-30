from . import bp as database
from app import db
from flask import jsonify, request, url_for, render_template, redirect
import requests, re, random
from .models import Event, Gauntlet, Trial, Participant, Influencer, Obstacle

@database.route('/main', methods=['GET'])
def main():
    return render_template('database/main.html')

@database.route('/tests', methods=['GET'])
def tests():
    return render_template('database/tests.html')

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

# populate event
@database.route('/populate_event', methods=['GET', 'POST'])
def populate_event():
    return render_template('database/populate_event.html')

# populate gauntlet
@database.route('/populate_gauntlet', methods=['GET', 'POST'])
def populate_gauntlet():
    return render_template('database/populate_gauntlet.html')

# populate trial
@database.route('/populate_trial', methods=['GET', 'POST'])
def populate_trial():
    return render_template('database/populate_trial.html')

# populate participant
@database.route('/populate_participant', methods=['GET', 'POST'])
def populate_participant():
    return render_template('database/populate_participant.html')

# populate influencer
@database.route('/populate_influencer', methods=['GET', 'POST'])
def populate_influencer():
    return render_template('database/populate_influencer.html')

# populate obstacle
@database.route('/populate_obstacle', methods=['GET', 'POST'])
def populate_obstacle():
    return render_template('database/populate_obstacle.html')