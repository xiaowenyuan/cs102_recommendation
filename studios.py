#Addresses randomly generated from https://www.fakeaddressgenerator.com/World_Address/popular_city/city/New%20York
#Names randomly generated from https://fossbytes.com/tools/random-name-generator 

from datetime import datetime, timedelta
from random import randrange, choice
import csv 
import pickle
from studio_classes import Activity, Activity_Time_Wrapper, Studio, Studio_List
from tree import BST, TreeNode

studio_list = Studio_List()

with open('random_names.csv', newline = '') as random_names_csv:
    names_reader = csv.DictReader(random_names_csv, delimiter = ',')
    names_list = []
    for row in names_reader:
        names_list.append(row['Names']) 

def add_timings(start, end):
    time_increments = [time for time in range(0, 60, 15)]
    result = []
    for i in range(start, end):
        for time in time_increments:
            result.append(time + i*100)
    return result

def generate_activities(studio, dictionary, list_of_timings, names_list):
    duration_options = [0.75, 1, 1.5]
    price_options = [price for price in range(10, 50, 5)]
    studio_instructors = []
    random_price = choice(price_options)
    for i in range(randrange(5,11)):
        possible_instructor = choice(names_list)
        studio_instructors.append(possible_instructor)
        names_list = [name for name in names_list if name != possible_instructor]
    for timings in list_of_timings:
        remaining_timings = timings.copy()
        if timings == afternoon_timings or timings == morning_timings:
            random_number_of_classes = randrange(0, 3)
        else:
            random_number_of_classes = randrange(0, len(timings))
        for _ in range(random_number_of_classes):
            if len(remaining_timings) == 0:
                break
            random_class_title = choice(list(dictionary.keys()))
            random_class_tags = dictionary[random_class_title]
            random_start_time = choice(remaining_timings)
            remaining_timings = [timing for timing in remaining_timings if 15 < abs(random_start_time - timing)]
            random_start_time = str(random_start_time)
            random_duration = choice(duration_options)
            random_instructor = choice(studio_instructors)
            names_list = [name for name in names_list if name != random_instructor]
            studio.add_activities(random_class_title, random_start_time, random_duration, random_class_tags, random_price, random_instructor)

def initialise_studio(studio, dictionary, list_of_timings, names_list = names_list):
    studio_list.add_studio(studio)
    generate_activities(studio, dictionary, list_of_timings, names_list)

morning_timings = add_timings(5,10)
afternoon_timings = add_timings(12,14)
special_afternoon_timings = add_timings(14, 16)
special_morning_timings = add_timings(4, 6)
evening_timings = add_timings(17,22)
list_of_timings = [morning_timings, afternoon_timings, evening_timings]
list_of_special_timings = [morning_timings, afternoon_timings, special_afternoon_timings, evening_timings, special_morning_timings]

#yoga studio 1: Eka Yoga
eka_yoga = Studio("Eka Yoga", "2056 Dancing Dove Lane")
#make dictionary of classes and tags 
eka_dict = {"Hatha Yoga": ["yoga", "hatha yoga", "stretch"], "Ashtanga Yoga": ["yoga", "ashtanga yoga", "stretch"], "Yin Yoga": ["yin yoga", "yoga", "stretch"], "Yoga Flow": ["yoga", "stretch"], "Hot Yoga": ["yoga", "hot yoga", "stretch"]}
initialise_studio(eka_yoga, eka_dict, list_of_timings)
#yoga studio 2: FRDM Yoga and Pilates
frdm_yoga = Studio("FRDM Yoga and Pilates", "2250 Godfrey Road")
frdm_dict = {
    "Bikram Yoga": ["yoga", "bikram yoga", "hot yoga", "stretch"],
    "Hatha Yoga": ["yoga", "hatha yoga", "stretch"],
    "Yoga Flow": ["yoga", "stretch"],
    "Mat Pilates": ["pilates", "mat pilates"], 
    "Stott Pilates": ["pilates", "stott pilates"], 
    "Reformer Pilates": ["pilates", "reformer pilates"], 
    "Yoga Pilates": ["yoga", "pilates", "mat pilates"],
    "Rocket Yoga": ["yoga", "rocket yoga", "stretch", "strength"]
}
initialise_studio(frdm_yoga, frdm_dict, list_of_special_timings)

#gym 1: 24/7 Fitness (offer yoga and bootcamp)
twentyfourseven_gym= Studio("24/7 Fitness", "1344 Bell Street")
twentyfour_dict = {
    "Bootcamp": ["bootcamp", "circuit training", "strength", "HIIT"], 
    "Hatha Yoga": ["yoga", "hatha yoga", "stretch"],
    "Vinyasa Yoga": ["yoga", "stretch"],
    "Mat Pilates": ["pilates", "mat pilates"],
    "Zumba": ["zumba", "dance", "cardio"], 
    "Pilloxing": ['cardio', 'boxing', 'pilates'],
    "Kickboxing": ['cardio', 'boxing', 'martial arts', 'kickboxing']
}
initialise_studio(twentyfourseven_gym, twentyfour_dict, list_of_special_timings)

#pole studio 1: XTAC Pole and Dance 
xtac_studio = Studio("XTAC Pole and Dance", "1825 Hoffman Avenue")
xtac_dict = {
    "Exo Flow": ["pole dance", "dance", "exotic dance"],
    "Striptease": ["pole dance", "dance", "exotic dance"],
    "Floorwork": ["dance", "exotic dance"],
    "Flexy": ["dance", "exotic dance", "stretch"],
    "Cardio Pole": ["dance", "exotic dance", "cardio"],
    "Pole Tricks": ["pole dance", "dance", "exotic dance"],
    "Inverts and Mounts": ["pole dance", "dance", "exotic dance"],
    "Lyrical Flow": ["pole dance", "dance", "exotic dance"],
    "Russian Pole": ["pole dance", "dance", "exotic dance"],
    "Beginner Pole": ["pole dance", "dance", "exotic dance"],
    "Static Pole": ["pole dance", "dance", "exotic dance"],
    "Heels Sensual": ["dance", "exotic dance"]
}
initialise_studio(xtac_studio, xtac_dict, list_of_timings)
#aerial studio: Soar Aerial Arts 
soar_arts = Studio("Soar Aerial Arts", "683 Bingamon Branch Road")
soar_dict = {
    "Exotic Pole": ["pole dance", "dance", "exotic dance"],
    "Lyrical Pole": ["pole dance", "dance", "exotic dance"],
    "Pole Level 1": ["pole dance", "dance", "exotic dance"],
    "Pole Level 2": ["pole dance", "dance", "exotic dance"],
    "Hoops Level 1": ["aerial", "hoops"],
    "Hoops Level 2": ["aerial", "hoops"],
    "Silk Level 1": ["aerial", "silk"],
    "Silk Level 2": ["aerial", "silk"],
    "Hammock Level 1": ["aerial", "hammock"],
    "Hammock Level 2": ["aerial", "hammock"],
    "Hoops Flow": ["aerial", "hoops", "dance"],
    "Silk Flow": ["aerial", "silk", "dance"],
    "Aerial Yoga": ['aerial', 'yoga', 'aerial yoga', 'stretch']
}
initialise_studio(soar_arts, soar_dict, list_of_timings)

#dance studio: Pointe studio 
pointe_studio = Studio("Pointe Dance Studio", "4428 Angus Road")
pointe_dict = {
    "Jazz Dance Level 1": ["dance", "cardio", "jazz"],
    "Jazz Dance Level 2": ["dance", "cardio", "jazz"],
    "Adult Ballet Level 1": ["dance", "cardio", "ballet"],
    "Adult Ballet Level 2": ["dance", "cardio", "ballet"],
    "Adult Ballet Level 3": ["dance", "cardio", "ballet"],
    "Tap dance": ["dance", "cardio", "tap dance"],
    "Zumba": ["zumba", "dance", "cardio"],
    "Contemporary Dance": ["contemporary dance", "dance", "cardio"],
    "Hip Hop": ["hip hop", "dance", "cardio"],
    "K-Pop": ["K-pop", "dance", "cardio"],
    "Dance cardio": ["dance", "cardio"],
}
initialise_studio(pointe_studio, pointe_dict, list_of_special_timings)

#crossfit gym: True Strength Gym
true_strength = Studio("True Strength Gym", "3428 Henry Ford Avenue")
true_dict= {
    "Metcon": ["strength", "conditioning", "metcon", "HIIT", "circuit"],
    "RKC Challenge":["kettlebell","strength", "conditioning", "HIIT", "circuit"],
    "Olympic Weightlifting": ["barbell", "strength", "conditioning", "HIIT"],
    "Obstacle Course": ["strength", "conditioning", "HIIT", "circuit"],
    "Power": ["strength", "conditioning", "HIIT", "circuit"],
    "Crossfit": ["strength", "conditioning", "crossfit", "HIIT", "circuit"],
}
initialise_studio(true_strength, true_dict, list_of_timings)
#gym 2: Barbell Lab
barbell_lab = Studio("Barbell Lab", "2647 Simons Hollow Road")
barbell_dict= {
    "Conditioning": ["strength", "conditioning", "metcon", "HIIT", "circuit"],
    "Kettlebells":["kettlebell","strength", "conditioning", "HIIT", "circuit"],
    "Olympic Weightlifting": ["barbell", "strength", "conditioning", "HIIT", "circuit"],
    "Barbell Beginners": ["barbell", "strength", "conditioning"],
    "Strength Circuit": ["strength", "conditioning", "metcon", "HIIT", "circuit"],
    "Power Yoga": ["yoga", "power yoga", "stretch"],
    "Mobility": ["stretch", "mobility"]
}
initialise_studio(barbell_lab, barbell_dict, list_of_timings)
#gym 3: Zoom Calisthenics and Parkour
zoom_movement = Studio("Zoom Movement", "717 Rosewood Lane")
zoom_dict = {
    "Handstands": ["gymnastics", "calisthenics", "bodyweight", "strength"],
    "Muscle-Ups": ["gymnastics", "calisthenics", "bodyweight", "strength"],
    "Planches": ["gymnastics", "calisthenics", "bodyweight", "strength"],
    "Manna": ["gymnastics", "calisthenics", "bodyweight", "strength"],
    "Front and Back Lever": ["gymnastics", "calisthenics", "bodyweight", "strength"],
    "Parkour Training": ['Parkour', "Free Running", "calisthenics"],
    "Parkour / Flip": ['Parkour', "Free Running", "calisthenics"],
    "Parkour Conditioning": ['Parkour', "Free Running", "calisthenics", "strength"],
    "Hatha Yoga": ["yoga", "hatha yoga", "stretch"]
}
initialise_studio(zoom_movement, zoom_dict, list_of_timings)

#gym 4
gold_standard = Studio("Gold Standard Studio", "2030 Mount Tabor")
gold_dict = {
    "Handstands": ["gymnastics", "calisthenics", "bodyweight", "strength"],
    "Calisthenic Pulls": ["gymnastics", "calisthenics", "bodyweight", "strength"],
    "Calisthenic Pushes": ["gymnastics", "calisthenics", "bodyweight", "strength"],
    "Tumbling": ["gymnastics", "calisthenics", "bodyweight", "strength", "tumbling"],
    "Parallettes": ["gymnastics", "calisthenics", "strength"],
    "Rings": ["gymnastics", "calisthenics", "strength"],
    "Bodyweight Circuit": ["HIIT", "calisthenics", "bodyweight", "conditioning"],
    "Jump Rope Fitness": ["HIIT", "cardio", "conditioning", "jump rope", "skipping"],
    "Yoga Pilates": ["yoga", "pilates", "mat pilates"],
    "Hatha Yoga": ["yoga", "hatha yoga", "stretch"]
}
initialise_studio(gold_standard, gold_dict, list_of_timings)
#spin 1: The Burn
burn_spin = Studio("The Burn", "4765 Geneva Street")
burn_dict = {
    "Ride": ["spin", "cycling", "cardio", "HIIT"],
    "Circuitbreaker": ["spin", "cycling", "cardio", "circuit", "conditioning", "HIIT"],
    "Ride Hard": ["spin", "cycling", "cardio", "HIIT"],
    "Yoga Flow": ["yoga", "stretch"],
    "Afterburn": ["spin", "cycling", "cardio", "circuit", "conditioning", "HIIT"]
}
initialise_studio(burn_spin, burn_dict, list_of_timings)

#pilates: Poise 
poise_pilates = Studio("Poise", "2469 Forest Avenue")
poise_dict = {
    "Mat Pilates": ["pilates", "mat pilates"], 
    "Stott Pilates": ["pilates", "stott pilates"], 
    "Reformer Pilates": ["pilates", "reformer pilates"], 
    "Yoga Pilates": ["yoga", "pilates", "mat pilates"], 
    "Contemporary Pilates": ["pilates", "contemporary pilates"]
}
initialise_studio(poise_pilates, poise_dict, list_of_special_timings)

#trampoline: Five Again Bounce Studio
recess = Studio("Recess Bounce Studio", "4239 Church Street")
recess_dict = {
    "Bounce Level 1": ["Trampoline", "Bounce", "Cardio", "Conditioning", "HIIT"],
    "Bounce Level 2": ["Trampoline", "Bounce", "Cardio", "Conditioning", "HIIT"],
    "Bounce Strength": ["Trampoline", "Bounce", "Strength", "Conditioning", "HIIT", "Circuit"],
    "Bounce HIIT": ["Trampoline", "Bounce", "Cardio", "Conditioning", "HIIT"],
    "Hatha Yoga": ["yoga", "hatha yoga", "stretch"],
    "Skip!": ["HIIT", "cardio", "conditioning", "jump rope", "skipping"],
    "Kickboxing": ['cardio', 'boxing', 'martial arts', 'kickboxing']
}
initialise_studio(recess, recess_dict, list_of_special_timings)
#gym 5: Uplift
uplift_gym = Studio("Uplift", "2770 Hanover Street")
uplift_dict = {
    "Vinyasa Flow": ["yoga", "stretch"],
    "Barbell Techniques": ["barbell", "strength", "conditioning"],
    "Olympic Weightlifting": ["barbell", "strength", "conditioning"],
    "Kettlebell Beginners": ["kettlebell", "strength", "conditioning"],
    "MetCon": ["metcon", "strength", "conditioning", "circuit", "HIIT"]
}
initialise_studio(uplift_gym, uplift_dict, list_of_special_timings)
#dance 2: Allegro Fitness and Dance 
allegro_dance = Studio("Allegro Fitness and Dance", "655 Patterson Road")
allegro_dict = {
    "Jazz": ["dance", "cardio", "jazz"],
    "Salsa": ["dance", "cardio", "salsa"],
    "Popping": ["dance", "cardio", "popping"],
    "Locking": ["dance", "cardio", "locking"],
    "Tap dance": ["dance", "cardio", "tap dance"],
    "Zumba": ["zumba", "dance", "cardio"],
    "Contemporary Dance": ["contemporary dance", "dance", "cardio"],
    "Hip Hop": ["hip hop", "dance", "cardio"],
    "K-Pop": ["K-pop", "dance", "cardio"],
    "Dance fitness": ["dance", "cardio"],
    "Heels": ["dance", "exotic dance"],
    "Body Combat": ["cardio", "martial arts"]
}
initialise_studio(allegro_dance, allegro_dict, list_of_timings)
#dance / yoga: ABC Community Center (line dance, salsa, taichi, yoga)
community_center = Studio("Bell Community Center", "4920 Bell Street")
community_dict = {
    "Taichi": ["taichi", "stretch"],
    "Line Dance": ["dance", "line dance"],
    "Salsa": ["ballroom", "dance", "salsa"],
    "Hatha Yoga": ["yoga", "hatha yoga", "stretch"],
    "Yoga for Seniors": ["yoga", "stretch"],
    "Mat Pilates": ["pilates", "mat pilates"],
    "Zumba": ["zumba", "dance", "cardio"], 
    "Pilloxing": ['cardio', 'boxing', 'pilates'],
    "Taichi for Beginners": ["taichi", "stretch"]
}
initialise_studio(community_center, community_dict, list_of_special_timings)
#spin 2: Unleashed Spin Studio
unleashed_spin = Studio("Unleashed Spin Studio", "2439 Pride Avenue")
unleashed_dict = {
    "Ride": ["spin", "cycling", "cardio", "HIIT"],
    "Ride and Rock": ["spin", "cycling", "cardio", "circuit", "conditioning", "HIIT"],
    "Ride+": ["spin", "cycling", "cardio", "HIIT"],
    "Raw power": ["strength", "HIIT", "circuit"],
    "Highway": ["spin", "cycling", "cardio", "circuit", "conditioning", "HIIT"]
}
initialise_studio(unleashed_spin, unleashed_dict, list_of_timings)
#combat 1: Silverback Boxing 
silverback_boxing = Studio("Silverback Boxing", "4864 Cantebury Drive")
silverback_dict = {
    "Boxing": ["boxing", "martial arts", "self defense"],
    "Fighter Conditioning": ["HIIT", "metcon", "conditioning", "martial arts"],
    "Boxing for Women": ["boxing", "martial arts", "self defense"],
    "White Collar Boxing": ["boxing", "martial arts", "self defense"],
    "Cardio Boxing": ["boxing", "cardio", "HIIT", "martial arts"],
    "Yoga for Fighters": ["yoga", "stretch"]
}
initialise_studio(silverback_boxing, silverback_dict, list_of_special_timings)
#combat 2: Knockout Fitness
knockout_fitness = Studio("Knockout Fitness", "1182 Williams Avenue")
knockout_dict = {
    "Boxing Circuit": ["bootcamp", "circuit training", "strength", "HIIT"], 
    "Hatha Yoga": ["yoga", "hatha yoga", "stretch"],
    "Boxing": ['cardio', 'boxing', 'martial arts', 'kickboxing'],
    "Ten Rounds": ['cardio', 'boxing', 'martial arts', 'kickboxing', "HIIT"],
    "Kickboxing": ['cardio', 'boxing', 'martial arts', 'kickboxing']
}
initialise_studio(knockout_fitness, knockout_dict, list_of_special_timings)
#combat 3: Ukemi MMA
ukemi_mma = Studio("Ukemi MMA", "262 Terry Lane")
ukemi_dict = {
    "BJJ for Beginners": ["bjj", "jiujitsu", "brazilian jiujitsu", "self defense", "martial arts", "grappling"],
    "BJJ Open": ["bjj", "jiujitsu", "brazilian jiujitsu", "self defense", "martial arts", "grappling"],
    "Judo for Beginners": ["judo", "self defense", "martial arts", "grappling"],
    "Judo Open": ["judo", "self defense", "martial arts", "grappling"],
    "MMA for Beginners": ["mixed martial arts", "self defense", "martial arts", "grappling", "MMA", "striking"],
    "MMA Open": ["mixed martial arts", "self defense", "martial arts", "grappling", "MMA", "striking"],
    "MMA Sparring": ["mixed martial arts", "self defense", "martial arts", "grappling", "MMA", "striking"],
    "Greco-Roman Wrestling": ["wrestling", "self defense", "martial arts", "grappling"],
    "Fighting Fit Conditioning": ["HIIT", "metcon", "conditioning", "martial arts"],
    "Muay Thai for Beginners": ["striking", "muay thai", "kickboxing", "self defense", "martial arts"],
    "Muay Thai Open": ["striking", "muay thai", "kickboxing", "self defense", "martial arts"],
    "Yoga for Athletes": ['yoga', 'stretch']
}
initialise_studio(ukemi_mma, ukemi_dict, list_of_special_timings)
#combat 4: Talon Combat and Self Defense 
talon_combat = Studio("Talon Combat and Self Defense", "4028 Oral Lake Road")
talon_dict = {
    "Boxing": ["boxing", "martial arts", "self defense"],
    "Self Defense for Women": ["krav maga", "systema", "martial arts", "self defense"],
    "Self Defense": ["krav maga", "systema", "martial arts", "self defense"],
    "Sambo": ["mixed martial arts", "self defense", "martial arts", "grappling", "MMA", "sambo"],
    "Brazilian Jiu Jitsu": ["bjj", "jiujitsu", "brazilian jiujitsu", "self defense", "martial arts", "grappling"],
    "Wing Chun": ["wing chun", "kung fu", "martial arts", "self defense"]
    }
initialise_studio(talon_combat, talon_dict, list_of_special_timings)
#climbing: Altitude
altitude_gym = Studio("Altitude", "2666 Patterson Road")
altitude_dict = {
    "Bouldering 101": ["bouldering", "climbing"],
    "Bouldering 102": ["bouldering", "climbing"],
    "Cardio Bouldering": ["bouldering", "climbing", "cardio"],
    "Climbing Conditioning": ["HIIT", "climbing", "conditioning", "circuit"],
    "Yoga for Climbers": ["yoga", "stretch"],
    "Top-Rope Climbing 101": ["climbing", "top-rope"],
    "Lead Climbing 101": ["climbing", "top-rope"],
    "Belaying Certification": ["climbing"],
    "Abseilling 101": ["climbing", "abseilling"]
}
initialise_studio(altitude_gym, altitude_dict, list_of_special_timings)

#compile all the tags into a set in the Studio List class

studio_list.compile_tags()

#test
print(studio_list.show_studios())
print(len(studio_list.show_studios()))
print(studio_list.get_tags())

search_tree = BST()
search_tree.update_from_database(studio_list)
search_tree.depth_first_traversal()

#pickle the studio list object instance 
with open('tree.p', 'wb') as pickle_file:
    pickle.dump(search_tree, pickle_file)

test1 = Activity(altitude_gym, "Climb", "1700", 1, ['climbing'], 0, 'John')
test2 = Activity(altitude_gym, "Climb", "1700", 1, ['climbing'], 0, 'Mary')

test1wrapped = Activity_Time_Wrapper(test1)
test2wrapped = Activity_Time_Wrapper(test2)

