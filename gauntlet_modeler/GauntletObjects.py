import requests, math, random

class Gauntlet:
    def __init__(self, owner_id=0):
        self.owner_id = owner_id
        self.id = 0
        self.name = 'Default_Name'
        self.trials = []
        self.class_time = 0
        self.class_days = 0
        self.weekend_days = 0
        self.extra_days = 0
        self.total_days = 0
        self.total_time = 0
        self.difficulty = 0
        self.description = 'Default_Description'
        
    def __repr__(self):
        return f'<Gauntlet | Name: {self.name} | Owner: {self.owner_id}>'
    
    def reset(self):
        trials_time = sum(trial.duration for trial in self.trials)
        self.class_time = trials_time
        self.class_days = math.ceil(self.class_time / 480)
        self.weekend_days = math.ceil(((self.class_days+ self.extra_days) / 5) * 2)
        self.total_days = self.weekend_days + self.class_days + self.extra_days
        self.total_time = self.total_days * 1440
        
        self.difficulty = sum(trial.difficulty for trial in self.trials) / len(self.trials)
        
    def set_id(self, idno):
        self.id = idno
    
    def set_name(self, name):
        self.name = name
        
    def set_extra_days(self, days):
        self.extra_days = days
        self.reset()
    
    def add_extra_days(self, days):
        self.extra_days += days
        self.reset()
    
    def set_trials(self, trials_list):
        self.trials = trials_list
        self.reset()
        
    def add_trials(self, trials_list):
        for trial in trials_list:
            self.trials.append(trial)
        self.reset()
        
    def set_description(self, description):
        self.description = description
    
    def randomize(self, trials_list, quantity):
        for i in range(0, quantity - 1):
            rand_num = random.randint(0, len(trials_list)-1)
            self.trials.append(trials_list[rand_num])
        self.reset()
    
class Trial:
    def __init__(self, owner_id=0):
        self.owner_id = owner_id
        self.id = 0
        self.name = 'Default Name'
        self.description = 'Default Description'
        self.difficulty = 1
        self.duration = 0
        
    def __repr__(self):
        return f'<Trial | Name: {self.name} | Owner ID: {self.owner_id}>'
    
    def set_id(self, idno):
        self.id = idno
        
    def set_name(self, name):
        self.name = name
    
    def set_description(self, description):
        self.description = description
        
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
    
    def set_duration(self, unit, quantity):
        if unit == 'days':
            self.duration = quantity * 1440
        elif unit == 'minutes':
            self.duration = quantity

def trial_from_dict(trial):
    new_trial = Trial()
    new_trial.set_name(trial['name'])
    new_trial.set_description(trial['description'])
    new_trial.set_difficulty(trial['difficulty'])
    new_trial.set_duration('seconds', trial['duration'])
    
    return new_trial

class Participant:
    def __init__(self, owner_id=0, attributes={}):
        self.owner_id = owner_id
        self.id = 0
        self.first_name = 'Default_First'
        self.last_name = 'Default_Last'
        self.attributes = attributes
        
    def __repr__(self):
        return f'<Participant | ID: {self.id} | Owner ID: {self.owner_id}>'
    
    def set_id(self, idno):
        self.id = idno
    
    def set_first_name(self, name):
        self.first_name = name
        
    def set_last_name(self, name):
        self.last_name = name
        
    def add_attribute(self, name, num):
        self.attributes[name] = num
    
    def delete_attribute(self, name):
        del self.attributes[name]
        
    def randomize(self, attributes_dict):
        for k,v in attributes_dict.items():
            random_val = random.randint(1, v)
            self.attributes[k] = random_val

def participant_from_dict(participant):
    new_participant = Participant()
    new_participant.set_id(participant['id'])
    new_participant.set_first_name(participant['name_1'].replace(' ', '_'))
    new_participant.set_last_name(participant['name_2'].replace(' ', '_'))
    new_participant.add_attribute('intellect', participant['attribute_1'])
    new_participant.add_attribute('endurance', participant['attribute_2'])
    new_participant.add_attribute('volatility', participant['attribute_3'])
    new_participant.add_attribute('background', participant['attribute_4'])
    new_participant.add_attribute('experience', participant['attribute_5'])
    return new_participant

class Team:
    def __init__(self, owner_id = 0):
        self.id = 0
        self.owner_id = owner_id
        self.name = 'Default_Name'
        self.participants = []
        
    def __repr__(self):
        return f'<Team | ID: {self.id} | Owner ID: {self.owner_id}>'
        
    def set_id(self, idno):
        self.id = idno
        
    def set_name(self, name):
        self.name = name
    
    def set_participants(self, participants):
        self.participants = participants
        
    def add_participant(self, participant):
        self.participants.append(participant)
        
    def remove_participant(self, participant_identifier):
        for participant in self.participants:
            if participant.id == participant_identifier or participant.first_name == participant_identifier:
                self.participants.remove(participant)
                
    def randomize(self, participants, quantity):
        self.participants = []
        for i in range(0, quantity - 1):
            rand_num = random.randint(0, len(participants)-1)
            self.participants.append(participants[rand_num])

class Influencer:
    def __init__(self, owner_id=0, attributes={}):
        self.owner_id = owner_id
        self.id = 0
        self.first_name = 'Default_First'
        self.last_name = 'Default_Last'
        self.attributes = attributes
        
    def __repr__(self):
        return f'<Influencer | ID: {self.id} | Owner ID: {self.owner_id}>'
    
    def set_id(self, idno):
        self.id = idno
    
    def set_first_name(self, name):
        self.first_name = name
        
    def set_last_name(self, name):
        self.last_name = name
        
    def add_attribute(self, name, num):
        self.attributes[name] = num
    
    def delete_attribute(self, name):
        del self.attributes[name]
        
    def randomize(self, attributes_dict):
        for k,v in attributes_dict.items():
            random_val = random.randint(1, v)
            self.attributes[k] = random_val

def influencer_from_dict(influencer):
    new_influencer = Influencer()
    new_influencer.set_id(influencer['id'])
    new_influencer.set_first_name(influencer['name_1'].replace(' ', '_'))
    new_influencer.set_last_name(influencer['name_2'].replace(' ', '_'))
    new_influencer.add_attribute('quality', influencer['attribute_1'])
    new_influencer.add_attribute('commitment', influencer['attribute_2'])
    new_influencer.add_attribute('volatility', influencer['attribute_3'])
    new_influencer.add_attribute('availability', influencer['attribute_4'])
    return new_influencer

class Event:
    def __init__(self, gauntlet, owner_id=0):
        self.owner_id = owner_id
        self.id = 0
        self.name = 'Default_Name'
        self.description = 'Default_Description'
        self.gauntlets = [gauntlet]
        self.teams = []
        self.influencers = []
        self.obstacles = []
        self.class_time = sum([gauntlet.class_time for gauntlet in self.gauntlets])
        self.class_days = sum([gauntlet.class_days for gauntlet in self.gauntlets])
        self.total_days = sum([gauntlet.total_days for gauntlet in self.gauntlets])
        self.total_time = sum([gauntlet.total_time for gauntlet in self.gauntlets])
        self.difficulty = sum([gauntlet.difficulty for gauntlet in self.gauntlets]) / len(self.gauntlets)
        
    def __repr__(self):
        return f'<Event | ID: {self.id} | Owner ID: {self.owner_id}>'
    
    def set_time(self):
        self.class_time = sum([gauntlet.class_time for gauntlet in self.gauntlets])
        self.class_days = sum([gauntlet.class_days for gauntlet in self.gauntlets])
        self.total_days = sum([gauntlet.total_days for gauntlet in self.gauntlets])
        self.total_time = sum([gauntlet.total_time for gauntlet in self.gauntlets])
        self.difficulty = sum([gauntlet.difficulty for gauntlet in self.gauntlets]) / len(self.gauntlets)
    
    def set_id(self, idno):
        self.id = idno
    
    def set_name(self, name):
        self.name = name
        
    def set_description(self, description):
        self.description = description
        
    def set_gauntlets(self, gauntlets):
        self.gauntlets = gauntlets
        self.set_time()
        
    def add_gauntlet(self, gauntlet):
        self.gauntlets.append(gauntlet)
        self.set_time()
        
    def remove_gauntlet(self, gauntlet_identifier):
        if len(self.gauntlets) <= 1:
            return f'Must have at least 1 gauntlet in an event!'
        else:
            for gauntlet in self.gauntlets:
                if gauntlet.id == gauntlet_identifier or gauntlet.name == gauntlet_identifier:
                    self.gauntlets.remove(gauntlet)
        self.set_time()
        
    def set_teams(self, teams):
        self.teams = teams
        
    def add_team(self, team):
        self.teams.append(team)
        
    def remove_team(self, team_identifier):
        for team in self.teams:
            if team.id == team_identifier or team.name == team_identifier:
                self.teams.remove(team)
        
    def set_influencers(self, influencers):
        self.influencers = influencers
        
    def add_influencer(self, influencer):
        self.influencers.append(influencer)
        
    def remove_influencer(self, influencer_identifier):
        for influencer in self.influencers:
            if influencer.id == influencer_identifier or influencer.first_name == influencer_identifier:
                self.influencers.remove(influencer)
                
    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        
    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)
        
    def remove_obstacle(self, obstacle_identifier):
        for obstacle in self.obstacles:
            if obstacle.id == obstacle_identifier or obstacle.name == obstacle_identifier:
                self.obstacles.remove(obstacle)
                
    def randomize(self, gauntlet_pool, team_pool, team_quantity, influencer_pool, influencer_quantity):

        self.gauntlets = []
        self.teams = []
        self.influencers = []
        self.obstacles = []
        
        random_gauntlet = gauntlet_pool[random.randint(0, len(gauntlet_pool)-1)]
        self.gauntlets = [random_gauntlet]
        
        random_teams = []
        team_count = 0
        while team_count < team_quantity:
            random_team = team_pool[random.randint(0, len(team_pool)-1)]
            random_teams.append(random_team)
            team_count += 1
        self.teams = random_teams
        
        random_influencers = []
        influencer_count = 0
        while influencer_count < influencer_quantity:
            random_influencer = influencer_pool[random.randint(0, len(influencer_pool)-1)]
            random_influencers.append(random_influencer)
            influencer_count += 1
            
        self.set_time()

def get_random_participant(participants):
    random_number = random.randint(0, len(participants)-1)
    return participants[random_number]

def get_random_team(teams):
    random_number = random.randint(0, len(teams)-1)
    return teams[random_number]
    
def get_random_influencer(influencers):
    random_number = random.randint(0, len(influencers)-1)
    return influencers[random_number]

def get_random_trial(trials):
    random_number = random.randint(0, len(trials)-1)
    return trials[random_number]

def get_random_gauntlet(gauntlets):
    random_number = random.randint(0, len(gauntlets)-1)
    return gauntlets[random_number]

def get_random_event(events):
    random_number = random.randint(0, len(events)-1)
    return events[random_number]

class GauntletEntities:
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.events = []
        self.participants = []
        self.teams = []
        self.influencers = []
        self.trials = []
        self.gauntlets = []
        self.runs = []
        self.random_words = requests.get('https://random-word-api.herokuapp.com/word?number=1000').json()
        
    def __repr__(self):
        return f'<Gauntlet Entities Object>'
    
    def generate_random_words(self, quantity):
        print('Generating Random Words')
        count = 0
        word_list = []
        while count < quantity:
            word_list.append(self.random_words[random.randint(0, 999)])
            count += 1
        return ' '.join(word_list)
    
    def create_participant(self, idno, first_name, last_name, attributes):
        new_participant = Participant(self.owner_id, attributes)
        new_participant.set_id(idno)
        new_participant.set_first_name(first_name)
        new_participant.set_last_name(last_name)
        
        self.participants.append(new_participant)
        
        return new_participant
    
    def generate_random_participants(self, quantity):
        print('Generating Participants')
        random_participants = []
        count = 0
        while count < quantity:
            print(f'{count + 1} Participants Generated')
            attributes_dict = {
                'intelligence':random.randint(1, 10),
                'endurance':random.randint(1, 10),
                'volatility':random.randint(1, 10),
                'background':random.randint(0, 288000)
            }
            attributes_dict['experience'] = attributes_dict['background']
            random_first = self.generate_random_words(1)
            random_last = self.generate_random_words(1)
            random_participants.append(self.create_participant(count, random_first, random_last, attributes_dict))
            count += 1
            
        return random_participants
    
    def create_team(self, idno, name, participants):
        new_team = Team(self.owner_id)
        new_team.set_id(idno)
        new_team.set_name(name)
        new_team.set_participants(participants)
        
        self.teams.append(new_team)
        
        return new_team
    
    def generate_random_team(self, team_size):
        print('Generating Team')
        team_participants = self.generate_random_participants(team_size)
        idno = sum([participant.attributes['background'] for participant in team_participants])
        name = self.generate_random_words(1)
        random_team = self.create_team(0, idno, team_participants)
        
        return random_team
    
    def create_influencer(self, idno, first_name, last_name, attributes):
        new_influencer = Influencer(self.owner_id, attributes)
        new_influencer.set_id(idno)
        new_influencer.set_first_name(first_name)
        new_influencer.set_last_name(last_name)
        
        self.influencers.append(new_influencer)
        
        return new_influencer
    
    def generate_random_influencers(self, quantity):
        print('Generating Influencers')
        random_influencers = []
        count = 0
        while count < quantity:
            print(f'{count + 1} Influencers Generated')
            attributes_dict = {
                'quality':random.randint(1, 10),
                'commitment':random.randint(1, 10),
                'volatility':random.randint(1, 10),
                'availability':random.randint(0, 2)
            }
            random_first = self.generate_random_words(1)
            random_last = self.generate_random_words(1)
            random_influencers.append(self.create_influencer(count, random_first, random_last, attributes_dict))
            
            count += 1
            
        return random_influencers
    
    def create_trial(self, idno, name, description, difficulty, duration):
        new_trial = Trial()
        new_trial.set_id(idno)
        new_trial.set_name(name)
        new_trial.set_description(description)
        new_trial.set_difficulty(difficulty)
        new_trial.set_duration('minutes', duration)
        
        self.trials.append(new_trial)
        
        return new_trial
        
    def generate_random_trials(self, quantity):
        print('Generating Trials')
        random_trials = []
        count = 0
        
        while count < quantity:
            print(f'{count+1} Trials Generated')
            random_name = self.generate_random_words(1)
            random_description = self.generate_random_words(10)
            random_difficulty = random.randint(1, 10)
            random_duration = random.randint(1, 10) * 1440
            random_id = random.randint(1, 1000000)
            random_trials.append(self.create_trial(random_id, random_name, random_description, random_difficulty, random_duration))
            count += 1
        
        return random_trials
    
    def create_gauntlet(self, idno, name, description, trials, extra_days):
        new_gauntlet = Gauntlet(self.owner_id)
        new_gauntlet.set_id(idno)
        new_gauntlet.set_name(name)
        new_gauntlet.set_description(description)
        new_gauntlet.set_trials(trials)
        new_gauntlet.set_extra_days(extra_days)
        
        self.gauntlets.append(new_gauntlet)
        
        return new_gauntlet
    
    def generate_random_gauntlet(self, gauntlet_size):
        print('Generating Gauntlet')
        random_name = self.generate_random_words(1)
        random_description = self.generate_random_words(10)
        random_extra = random.randint(0, 10)
        gauntlet_trials = self.generate_random_trials(gauntlet_size)
        random_id = random.randint(1, 1000000)
        
        random_gauntlet = self.create_gauntlet(random_id, random_name, random_description, gauntlet_trials, random_extra) 
        
        return random_gauntlet
    
    def create_event(self, idno, name, description, gauntlet, teams, influencers):
        new_event = Event(gauntlet, self.owner_id)
        new_event.set_id(idno)
        new_event.set_name(name)
        new_event.set_description(description)
        new_event.set_teams(teams)
        new_event.set_influencers(influencers)
        
        self.events.append(new_event)
        
        return new_event
    
    def generate_random_event(self, trial_quantity, team_quantity, team_size, influencer_quantity):
        print('Generating Event')
        random_id = random.randint(1, 1000000)
        random_name = self.generate_random_words(1)
        random_description = self.generate_random_words(10)
        random_gauntlet = self.generate_random_gauntlet(trial_quantity)
        
        random_teams = []
        team_count = 0
        while team_count < team_quantity:
            random_team = self.generate_random_team(team_size)
            random_teams.append(random_team)
            team_count += 1
            
        random_influencers = self.generate_random_influencers(influencer_quantity)
        
        
        random_event = self.create_event(random_id, random_name, random_description, random_gauntlet, random_teams, random_influencers)
        
        return random_event
    
    def randomize_event(self, event, gauntlet_pool, team_pool, influencer_pool):
        print('Randomizing Event')
        event.randomize(gauntlet_pool, team_pool, len(event.teams), influencer_pool, len(event.influencers))
