import GauntletObjects
from datetime import datetime
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
            new_run = EventRunner(self.current_event)
            new_run.start_run()
            run_object = new_run.create_run()
            run_object.set_columns()

            self.runs.append(run_object)
            return new_run
    
    def randomize_event_team(self, size=10):
        self.current_event.teams[0] = self.library.generate_random_team(size)
        
    def randomize_event_gauntlet(self, size=5):
        self.current_event.gauntlets[0] = self.library.generate_random_gauntlet(size)  

    def randomize_event_influencer(self):
        self.current_event.influencers = self.library.generate_random_influencers(1)      
        
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
            elif target == 'influencer':
                self.randomize_event_influencer()
                self.run_event()
            else:
                return 'Target Error'
            count += 1


    
class EventRunner:
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
                # print(participant)
                # Log Current Participant Values
                row_number += 1

                # Previous Version as Dictionary is commented out
                # results[row_number] = {}
                results[row_number] = []
                row = results[row_number]
                # row['index'] = row_number
                row.append(row_number) # i = 0
                # row['event'] = self.event.name
                row.append(self.event.name) # i = 1
                # row['gauntlet'] = self.gauntlet.name
                row.append(self.gauntlet.name) # i = 2
                # row['trial'] = current_trial.name
                row.append(current_trial.name) # i = 3
                # row['time'] = event_time
                row.append(event_time) # i = 4
                # row['day'] = current_day
                row.append(current_day) # i = 5
                # row['first_name'] = participant.first_name
                row.append(participant.first_name) # i = 6
                # row['last_name'] = participant.last_name
                row.append(participant.last_name) # i = 7

                current_status = self.participant_status(participant, current_time, is_weekend, is_class)
                row.append(current_status) # i = 8

                row.append(perfect_progress) # i = 9
                row.append(round(participant.attributes['major']/(perfect_progress+1), 2)) # i = 10
                row.append(self.influencer.first_name)
                row.append(self.influencer.last_name)
                row.append(self.influencer.attributes['attribute_1'])
                row.append(self.influencer.attributes['attribute_2'])
                for attribute, value in participant.attributes.items():
                    # row[attribute] = value
                    row.append(value)

                # row['perfect_progress'] = perfect_progress
                # row['participant_success'] = round(participant.attributes['major']/(perfect_progress+1), 2)
                
#                 print(f'Perfect Progress: {perfect_progress}')
#                 print(f"Participant Progress: {participant.attributes['major']}")
#                 print(f"Participant Success: {row['participant_success']}")
                
                # Change Participant Data
                # Determine Participant Status
                # row['participant_status'] = self.participant_status(participant, current_time, is_weekend, is_class)
                
#                 print(row['participant_status'])
                
                # Determine Participant Progress
                # participant.attributes['major'] += self.participant_progress(participant, row['participant_status'], is_class, influencer_active, current_trial)
                # print(f"Current Experience: {participant.attributes['major']}")
                progress = self.participant_progress(participant, current_status, is_class, influencer_active, current_trial)
                # print(f'Progress: {progress}')
                participant.attributes['major'] += progress
                # print(f"New Experince: {participant.attributes['major']}")
                
        real_end = datetime.now()
        print(f'End Time: {real_start}')    
        print(f'Test Time: {real_end - real_start}')
        print(f"Rows Generated: {len(self.results['data'])}")                                      
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
            trial_modifier = 1 / trial.difficulty
#             print(f'Trial Difficulty: {trial.difficulty}')
#             print(f'Trial Modifier: {trial_modifier}')
            intelligence_modifier = participant.attributes['minor_1'] / 10
            influencer_modifier = self.influencer.attributes['attribute_1'] / 10
            if influencer_active == False:
                influencer_modifier = 1

            progress = round(((100 * intelligence_modifier * trial_modifier) * (1 + influencer_modifier)), 2)
            # print(f'Calculated Progress: {progress}')
#             print(f'Status: {status}')
#         print(f'Progress: {progress}')
        return progress

    def create_run(self):
        new_run_object = Run(self.results, self.event)
        new_run_object.set_columns()

        return new_run_object

class Run:
    def __init__(self, run_data, event, name='Default_Name'):
        self.name = name
        self.run_data = run_data
        self.stats = run_data['stats']
        self.rows = run_data['data']
        self.columns = []
        self.event = event
        
    def __repr__(self):
        return f'<Run | Name: {self.name}>'
        
    def set_columns(self):
        data_points = ['row_number', 'event', 'gauntlet', 'trial', 'time', 'day', 'participant_first_name', 'participant_last_name', 'status', 'perfect_progress', 'success_value', 'influencer_first_name', 'influencer_last_name', 'influencer_attribute_1', 'influencer_attribute_2']

        for attribute in self.event.teams[0].participants[0].attributes.keys():
            data_points.append(f'participant_{attribute}')

        self.columns = data_points
        
    def set_name(self, name):
        self.name = name

class Visualizer:
    
    def __init__(self, runs):
        self.runs = runs
        self.dataframes = []
        self.figures = {}
        
    def runs_to_frame(self):
        for run in self.runs:
            columns = run.columns
            rows = run.run_data['data']

            new_frame = pd.DataFrame.from_dict(rows, orient='index', columns=columns)
            self.dataframes.append(new_frame)

class Final:
    def __init__(self, name, trial_quantity=5, team_size=10):
        self.name = name
        self.test_count = 0
        self.tests = {}
        self.trial_quantity = trial_quantity
        self.team_size = team_size

    def run_tests(self, quantity):
        count = 0
        while count < quantity:
            self.test_count += 1

            new_gauntlet = GauntletApp(0)
            new_gauntlet.new_random_event(self.trial_quantity, 1, self.team_size, 1)
            new_gauntlet.run_event()
            new_visualizer = Visualizer(new_gauntlet.runs)
            new_visualizer.runs_to_frame()
            this_frame = new_visualizer.dataframes[0]

            this_test = this_frame
            self.tests[self.test_count] = this_test

            # start_rows = this_frame.head(10)
            end_rows = this_frame.tail(self.team_size)
            
            print(f'Event:{new_gauntlet.current_event.name}')
            average_success = end_rows.success_value.mean()
            print(f'Average Success: {average_success}')
            
    #         participant_frames = []
    #         for participant_name in this_frame.participant_first_name.unique():
    #             participant_frame = this_frame[this_frame['participant_first_name'] == participant_name]
    #             participant_frame.reset_index(drop=True, inplace=True)
    #             participant_frames.append(participant_frame)
    #         for frame in participant_frames:
    #             success_frame = frame[frame['success_value'] <= .85]
    #             success_frame.plot.line(x='time', y='success_value')
                
            end_students = end_rows[['participant_first_name', 'participant_last_name', 'participant_minor_1', 'participant_minor_2', 'success_value']]
            passing_students = end_students[end_students['success_value'] > .5]
            failing_students = end_students[end_students['success_value'] < .5]
            print(f'Passing Intellect: {passing_students.participant_minor_1.mean()}')
            print(f'Passing Endurance: {passing_students.participant_minor_2.mean()}')
            print(f'Failing Intellect: {failing_students.participant_minor_1.mean()}')
            print(f'Failing Endurance: {failing_students.participant_minor_2.mean()}')
            
            greater_intellect = end_rows[end_rows['participant_minor_1'] >= end_rows['participant_minor_2']]
            greater_endurance = end_rows[end_rows['participant_minor_2'] >= end_rows['participant_minor_1']]
            print(f'Greater Intellect Success: {greater_intellect.success_value.mean()}')
            print(f'Greater Endurance Success: {greater_endurance.success_value.mean()}')
            
            above_int = end_rows[end_rows['participant_minor_1'] >= 5]
            above_end = end_rows[end_rows['participant_minor_2'] >= 5]
            below_int = end_rows[end_rows['participant_minor_1'] <= 5]
            below_end = end_rows[end_rows['participant_minor_2'] <= 5]
            
            print(f'Above Int Success: {above_int.success_value.mean()}')
            print(f'Above End Success: {above_end.success_value.mean()}')
            print(f'Below Int Success: {below_int.success_value.mean()}')
            print(f'Below End Success: {below_end.success_value.mean()}')
            
            print('=================================')
            
            count += 1