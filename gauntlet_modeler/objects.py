import requests, math, random

class Trial:
    def __init__(self, name, owner_id=0):
        self.owner_id = owner_id
        self.name = name
        self.description = ''
        self.difficulty = 1
        self.duration = 0
        
    def __repr__(self):
        return f'<Trial | Name: {self.name} | Owner ID: {self.owner_id}>'
        
    def set_name(self, name):
        self.name = name
    
    def set_description(self, description):
        self.description = description
        
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
    
    def set_duration(self, unit, quantity):
        if unit == 'days':
            self.duration = quantity * 28800
        elif unit == 'minutes':
            self.duration = quantity * 60
        elif unit == 'seconds':
            self.duration = quantity

def trial_from_dict(trial):
    new_trial = Trial(trial['name'])
    new_trial.set_description(trial['description'])
    new_trial.set_difficulty(trial['difficulty'])
    new_trial.set_duration('seconds', trial['duration'])
    
    return new_trial

class Gauntlet:
    def __init__(self, name, owner_id=0):
        self.owner_id = owner_id
        self.name = name
        self.trials = []
        self.class_time = 0
        self.class_days = 0
        self.weekend_days = 0
        self.extra_days = 0
        self.total_days = 0
        self.total_time = 0
        self.difficulty = 0
        self.description = ''
        
    def __repr__(self):
        return f'<Gauntlet | Name: {self.name} | Owner: {self.owner_id}>'
    
    def reset(self):
        trials_time = sum(trial.duration for trial in self.trials)
        self.class_time = int(trials_time / 60)
        self.class_days = math.ceil(self.class_time / 480)
        self.weekend_days = math.ceil(((self.class_days+ self.extra_days) / 5) * 2)
        self.total_days = self.weekend_days + self.class_days + self.extra_days
        self.total_time = self.total_days * 1440
        
        self.difficulty = sum(trial.difficulty for trial in self.trials) / len(self.trials)
    
    def set_name(self, new_name):
        self.name = new_name
        
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
            rand_num = random.randint(0, len(trials_list))
            self.trials.append(trials_list[rand_num])
        self.reset()

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
        for k,v in attributes_dict:
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
    