from datetime import datetime, time, timedelta 
import pickle
from time import strptime
from tree import BST, TreeNode
from studio_classes import Activity, Activity_Time_Wrapper, Studio, Studio_List
import heapq
from string import printable

with open('tree.p', 'rb') as pickle_file:
    tree = pickle.load(pickle_file)

debug_status = False

def debugprint(str):
    if debug_status:
        print(str)

def sort_classes_time(classes_list):
    heap = []
    for activity in classes_list:
        wrapped_activity = Activity_Time_Wrapper(activity)
        heapq.heappush(heap, wrapped_activity)
    return heap

def is_valid_time(user_input):
    if user_input == "0" or user_input == "00":
        print('\nPlease enter \'000\' if you meant to enter 12 midnight.')
        return False
    for char in user_input:
        if not char.isnumeric():
            return False
    if int(user_input) > 2359:
        return False
    if int(user_input[-2:]) > 59:
        return False
    if len(user_input) < 3:
        return False
    return True

def is_valid_end_time(start_time, user_input):
    if user_input == "0" or user_input == "00":
        print('\nPlease enter \'000\' if you meant to enter 12 midnight.')
        return False
    for char in user_input:
        if not char.isnumeric():
            return False
    if int(user_input) > 2359:
        return False
    if int(user_input[-2:]) > 59:
        return False
    if len(user_input) < 3:
        return False
    if int(user_input) <= int(start_time):
        print('\nPlease enter an end time that is later than the stipulated start time.')
        return False
    return True

def run_script():
    end_program = False
    print('\n#####################################################')
    print('\nWelcome to Sweat Search!')
    print('\n#####################################################')
    print('\nWe help you search for workout classes near you that are available during a convenient time of your choosing.')
    while end_program is False:
        search_input = input('\nType the beginning of the activity and press enter to see if it\'s here: ')
        print(f'\nSearching for activities that start with the letter(s) \'{search_input}\'')
        search_result = tree.autocomplete_search(search_input.lower())
        while len(search_result) > 1:
            print(f'\nHere are {len(search_result)} activities that start with the letter(s) \'{search_input}\': ')
            print('\n')
            print(search_result)
            search_input = input('\nIf you already know the activity you want, enter it here. Else, type the beginning of the activity and press enter to see if it\'s here: ')
            search_result = tree.autocomplete_search(search_input.lower())
        if len(search_result) == 0:
            print(f'\nThere are no activities that start with the letters \'{search_input}\'.')
            print('\nPlease try again.')
            continue
        if search_result[0].key == search_input:
            confirmed_yn = input(f'Would you like to look for classes that involve {search_result[0].key}? Enter \'Y\' to proceed, or \'N\' to restart the search: ').lower()
        else:
            print(f'The only activity that starts with the letter(s) \'{search_input}\' is: {search_result[0].key}')
            confirmed_yn = input(f'Would you like to look for classes that involve {search_result[0].key}? Enter \'Y\' to proceed, or \'N\' to restart the search: ').lower()
        while confirmed_yn != 'y' and confirmed_yn != 'n':
            confirmed_yn = input(f'Would you like to look for classes that involve {search_result[0].key}? Enter \'Y\' to proceed, or \'N\' to restart the search: ')
        if confirmed_yn == 'n':
            continue
        if confirmed_yn == 'y':
            result = search_result[0].payload
            print(f'\nWe found {len(result)} classes that involve {search_result[0].key}.')
        start_time = input('\nPlease insert the earliest time you would like to attend class at. Please use the 24 hour time format in HHMM (max time is 2359). For example, 8AM is 800 and 530PM is 1730: ')
        while is_valid_time(start_time) == False:
            print('\nSorry, that is an invalid entry.')
            start_time = input('\nPlease insert the earliest time you would like to attend class at. Please use the 24 hour time format in HHMM (max time is 2359). For example, 8AM is 800 and 530PM is 1730: ')
        end_time = input('\nPlease insert the latest time you would like the class to end by: ')
        while is_valid_end_time(start_time, end_time) == False:
            print('\nSorry, that is an invalid entry.')
            end_time = input('\nPlease insert the latest time you would like the class to end by: ')
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
            print(f'\n{len(filtered_result)} classes involve {search_result[0].key} and start at or after {start_time} and end at or before {end_time}')
            heap = sort_classes_time(filtered_result)
            for i in range(len(heap)):
                popped_activity_wrapped = heapq.heappop(heap)
                popped_activity_wrapped.activity.print_out()
        else:
            print(f'\nThere is no class that involves {search_result[0].key} that starts at or after {start_time} and ends at or before {end_time}')
        reset_input = input('\n Would you like to restart the search? Type Y to restart and N to quit the program: ').lower()
        if reset_input == "n":
            end_program = True
        while reset_input != "y":
            if reset_input == "n":
                end_program = True
                print('\nThank you for using Sweat Search!')
                print('\nWe hope to see you again!')
                break
            else:
                reset_input = input('\n Would you like to restart the search? Type Y to restart and N to quit the program: ')
        continue

run_script()


