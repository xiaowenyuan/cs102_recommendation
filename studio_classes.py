from datetime import datetime, timedelta

class Activity:
    activity_id = 0
    def __init__(self, studio, title, start_time, duration, tags, price, instructor):
        Activity.activity_id += 1
        self.activity_id = Activity.activity_id
        self.studio = studio
        self.title =  title
        self.tags = tags
        self.start_time = datetime.strptime(start_time, "%H%M")
        self.start_time_string = start_time
        self.duration = timedelta(hours = duration)
        self.end_time = self.start_time + self.duration
        self.price = price
        self.instructor = instructor
    
    def __repr__(self):
        return self.title + " at " + self.start_time_string + " at " + self.studio.studio_name
    
class Studio:
    studio_id = 0
    def __init__(self, studio_name, location):
        Studio.studio_id += 1
        self.studio_id = Studio.studio_id
        self.studio_name = studio_name
        self.location = location
        self.activities = []
        
    def add_activities(self, title, start_time, duration, tags, price, instructor):
        new_activity_instance = Activity(self, title, start_time, duration, tags, price, instructor)
        self.activities.append(new_activity_instance)

    def __repr__(self):
        return self.studio_name

    def show_activities_as_list(self):
        return self.activities()

    def show_activities(self):
        list_of_activities = []
        for activity in self.activities:
            row = {}
            row['title'] = activity.title
            row['start_time'] = activity.start_time
            row['duration'] = activity.duration
            row['price'] = activity.price
            row['instructor'] = activity.instructor
            row['tags']= activity.tags
            list_of_activities.append(row)
        return list_of_activities 

class Studio_List:
    def __init__(self):
        self.list_of_studios = []
        self.set_of_tags = set()

    def add_studio(self, studio):
        self.list_of_studios.append(studio)
    
    def show_studios(self):
        return self.list_of_studios
    
    def compile_tags(self):
        for studio in self.list_of_studios:
            for activity in studio.activities:
                for tag in activity.tags:
                    self.set_of_tags.add(tag.lower())
    
    def get_tags(self):
        return self.set_of_tags


    