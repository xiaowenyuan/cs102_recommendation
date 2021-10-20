from datetime import datetime, time, timedelta 
import pickle
from time import strptime
from tree import BST, TreeNode
from studio_classes import Activity, Studio, Studio_List

with open('tree.p', 'rb') as pickle_file:
    tree = pickle.load(pickle_file)

debug_status = True

def debugprint(str):
    if debug_status:
        print(str)

def run_script():
    print('\nWelcome to Sweat Search!')
    print('\nWe help you search for workout classes near you that are available during a convenient time of your choosing.')
    search_input = input('\nType in the type of activity that you are looking for: ')
    print(f'\nSearching for activities that involve {search_input}')
    result = tree.get(search_input)
    while result is None:
            print(f'\nThere are no activities that involve {search_input} at this time.')
            search_input = input('Please try another type of activity: ')
            print(f'\nSearching for activities that involve {search_input}')
            result = tree.get(search_input)
    if result:
        print(f'\nWe found some activities that involve {search_input}!')
        debugprint(result)
        start_time = input('Please insert the earliest time you would like to attend class at. Please use the 24 hour time format in HHMM. For example, 530PM is 1730: ')
        end_time = input('Please insert the latest time you would like the class to end by: ')
        #make a while loop to ensure that the start and end time inputs are valid inputs
        start_time_object = datetime.strptime(start_time, "%H%M")
        end_time_object = datetime.strptime(end_time, "%H%M")
        filtered_result = []
        for activity in result:
            debugprint(f'\nChecking {activity}')
            class_start_time = activity.start_time
            class_end_time = activity.end_time
            debugprint(f'{activity} starts at {class_start_time} and ends at {class_end_time}')
            if class_start_time >= start_time_object and class_end_time <= end_time_object:
                debugprint(f'Class found! {activity} starts after {start_time} and ends before {end_time}')
                filtered_result.append(activity)
        if filtered_result:
            debugprint('\nWe have some results!')
            debugprint(filtered_result)
            
run_script()