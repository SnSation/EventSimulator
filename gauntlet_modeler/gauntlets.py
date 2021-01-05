import GauntletObjects
from datetime import datetime

saved_data = []
class GauntletApp:
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.library = GauntletObjects.GauntletEntities(self.owner_id)
        self.runs = []
        self.current_event = None
        self.current_run = None
        
    def select_event(self, event_id):
        self.current_event = event_id ## NEEDS UPDATE
        
    def new_random_event(self, trial_quantity=5, team_quantity=1, team_size=10, influencer_quantity=1):
        self.library.generate_random_event(trial_quantity, team_quantity, team_size, influencer_quantity)
        self.current_event = self.library.events[-1]
    
    def run_event(self):
        if self.current_event == None:
            print('No Event Selected')
        else:
            print(f'Running Event: {self.current_event}')            
            new_run = EventRun(self.current_event)
            new_run.start_run()
            
            self.runs.append(new_run)
            return new_run
    
    def randomize_event_team(self, size=10):
        self.current_event.teams[0] = self.library.generate_random_team(size)
        
    def randomize_event_gauntlet(self, size=5):
        self.current_event.gauntlets[0] = self.library.generate_random_gauntlet(size)        
        
    def run_tests(self, quantity, target):
        self.new_random_event()
        count = 0
        while count < quantity:
            if target == 'team':
                self.randomize_event_team()
                self.run_event()
            elif target == 'gauntlet':
                self.randomize_event_gauntlet()
                self.run_event()
            else:
                return 'Target Error'
            count += 1
    
class EventRun:
    def __init__(self, event, team_index=0, gauntlet_index=0, influencer_index=0):
        self.event = event
        self.team = event.teams[team_index]
        self.gauntlet = event.gauntlets[gauntlet_index]
        self.influencer = event.influencers[influencer_index]
        self.duration = event.total_time
        self.results = {}
        
    def start_run(self):
        real_start = datetime.now()
        print(f'Start Time: {real_start}')
        # Get Stats
        self.results['stats'] = {}
        stats = self.results['stats']
        stats['influencer'] = self.influencer
        stats['gauntlet_difficulty'] = self.gauntlet.difficulty

        # Get Average Stats
        average_attributes = {}

        for participant in self.team.participants:
            for attribute, value in participant.attributes.items():
                if attribute in average_attributes.keys():
                    average_attributes[attribute] += value
                else:
                    average_attributes[attribute] = value

        for attribute, value in average_attributes.items():
            average_attributes[attribute] = value / len(self.team.participants)
        
        stats['average_attributes'] = average_attributes      

        # Event Run
        self.results['data'] = {}
        results = self.results['data']
        row_number = 0
        perfect_progress = 0
        current_time = 0
        
        event_time = 0
        event_duration = self.event.total_time
        
        # Event Flags
        event_running = True
        current_day = 1
        is_weekend = False
        is_class = False
        current_trial = self.gauntlet.trials[0]
        current_trial_index = 0
        influencer_active = False
        
        # Event Variables
        trial_time = 0

        # print(f'Starting Event:{self.event.name}')
        
        while event_running == True:
            event_time += 1
            current_time += 1
            trial_time += 1
            
#             print('\n')
#             print(f'Event Time: {event_time}')
#             print(f'Current Time: {current_time}')
#             print(f'Current Day: {current_day}')
#             print(f'Current Trial: {current_trial}')
#             print(f'Perfect Progress: {perfect_progress}')
#             print(f'Is Class? {is_class}')
#             print(f'Is Weekend? {is_weekend}')
#             print(f'Influencer Active? {influencer_active}')
            
            
            if event_time >= event_duration:
                event_running = False
            
            # Set Event Flags
            
            # Set current_day and current_time
            if event_time % 1440 == 0:
                current_day += 1
                current_time = 0
                
            # Set is_weekend Flag
            if current_day % 6 == 0 or current_day % 7 == 0:
                is_weekend = True
            else:
                is_weekend = False
                
            # Set is_class Flag
            if current_time > 540 and current_time < 1021 and is_weekend == False:
                is_class = True
                perfect_progress += 100
            else:
                is_class = False
                
            # Set influencer_active Flag
            if current_time > 540 and current_time < (1021 + self.influencer.attributes['attribute_2']*30):
                influencer_active = True
            else:
                influencer_active = False
            
            # Set Trial Data
            if trial_time == current_trial.duration:
                trial_time == 0
                current_trial_index += 1
                current_trial = self.gauntlet.trials[current_trial_index]
                        
            # Set Participant Data
            for participant in self.team.participants:
                print(participant)
                # Log Current Participant Values
                row_number += 1
                results[row_number] = {}
                row = results[row_number]
                row['index'] = row_number
                row['event'] = self.event.name
                row['gauntlet'] = self.gauntlet.name
                row['trial'] = current_trial.name
                row['time'] = event_time
                row['day'] = current_day
                row['first_name'] = participant.first_name
                row['last_name'] = participant.last_name
                for attribute, value in participant.attributes.items():
                    row[attribute] = value
                row['perfect_progress'] = perfect_progress
                row['participant_success'] = round(participant.attributes['major']/(perfect_progress+1), 2)
                
#                 print(f'Perfect Progress: {perfect_progress}')
#                 print(f"Participant Progress: {participant.attributes['major']}")
#                 print(f"Participant Success: {row['participant_success']}")
                
                # Change Participant Data
                # Determine Participant Status
                row['participant_status'] = self.participant_status(participant, current_time, is_weekend, is_class)
                
#                 print(row['participant_status'])
                
                # Determine Participant Progress
                participant.attributes['major'] += self.participant_progress(participant, row['participant_status'], is_class, influencer_active, current_trial)
                
                saved_data.append(results[row_number])

        real_end = datetime.now()
        print(f'End Time: {real_start}')    
        print(f'Test Time: {real_end - real_start}')                                      
        return self.results
    
    def participant_status(self, participant, current_time, is_weekend, is_class):
        max_time = participant.attributes['minor_2'] * 30 # each point of endurance = 30 minutes of working time
        if is_class == True:
            return 'working'
        elif is_weekend == True:
            if current_time < max_time:
                return 'working'
        elif (current_time > 1020) and (current_time - max_time) < 1020:
            return 'working'
        else:
            return 'resting'
            
    
    def participant_progress(self, participant, status, is_class, influencer_active, trial):        
        progress = 0
        if status == 'working':
            trial_modifier = (11 - trial.difficulty) / 10
#             print(f'Trial Difficulty: {trial.difficulty}')
#             print(f'Trial Modifier: {trial_modifier}')
            intelligence_modifier = participant.attributes['minor_1'] / 10
            influencer_modifier = self.influencer.attributes['attribute_1'] / 10
            if influencer_active == False:
                influencer_modifier = 1

            progress = (100 * intelligence_modifier * trial_modifier) * (1 + influencer_modifier)
#             print(f'Status: {status}')
#         print(f'Progress: {progress}')
        return progress

new_gauntlet = GauntletApp(0)
new_gauntlet.new_random_event()
print(new_gauntlet.current_event)
new_gauntlet.run_event()
print(new_gauntlet.runs[0])