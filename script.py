from datetime import time, timedelta
from math import inf

class Activity:
    activity_id = 0
    def __init__(self, title, start_time, duration, tags, price = 0, instructor = None, capacity = inf):
        Activity.activity_id += 1
        self.activity_id = Activity.activity_id
        self.title =  title
        self.tags = tags
        self.start_time = time.strptime(start_time, "%H%M")
        self.duration = timedelta(hour=duration)
        self.end_time = self.start_time + self.duration
        self.price = price
        self.instructor = instructor
        self.capacity = capacity
    
class Studio:
    studio_id = 0
    def __init__(self, studio_name, location, activities = None):
        Studio.studio_id += 1
        self.studio_id = Studio.studio_id
        self.studio_name = studio_name
        self.location = location
        self.activities = activities
        

    def add_activities(self, title, start_time, duration, tags, price = 0, instructor = None, capacity = inf):
        new_activity_instance = Activity(title, start_time, duration, tags, price, instructor, capacity)
        self.activities.append(new_activity_instance)

class BST:
    def __init__(self):
        self.root = None
        self.depth = 0 

    def get_bst_depth(self):
        return self.depth

    def insert(self, new_key, new_payload):
        #check if self.root exists
        if self.root:
            #if self.root exists, run the _insert function recursively
            self._insert(new_key, new_payload, self.root)
        #if self.root does not exist, make a new root
        else:
            print(f'No root exists. Creating a new node {new_key} at depth {self.depth}')
            self.root = TreeNode(new_key, new_payload)
            self.depth += 1
            return self.root

    def _insert(self,new_key, new_payload, current_node):
        #check if new_key < current_node.key --> checking left child 
        if new_key < current_node.key:
            #check if left child exists
            if current_node.has_left_child():
                self.depth += 1
                #if left_child exists run the insert method recursively with left_child as the current node now
                self._insert(new_key, new_payload, current_node.left_child)
            else:
                #if left_child does not exist then insert the key as the current node's left_child
                current_node.left_child = TreeNode(new_key, new_payload)
                print(f'Inserting new node {new_key} to the left of {current_node} at depth {self.get_bst_depth()}')
                return current_node.left_child
        #check if new_key > self.root.key --> checking right child
        elif new_key > current_node.key:
            #check if right child exists
            if current_node.has_right_child():
                self.depth += 1
                #if right_child exists, run the insert method recursively with right_child as current node
                self._insert(new_key, new_payload, current_node.right_child)
            else:
                #if right_child does not exist, insert the key as current node's right_child
                current_node.right_child = TreeNode(new_key, new_payload)
                print(f'Inserting new node {new_key} to the right of {current_node} at {self.get_bst_depth()}')
                return current_node.right_child
        #if new_key == current_node.key, update the key with the new payload
        else:
            print(f'Updating {current_node} node\'s payload to include {new_payload}. {current_node} payload is now:')
            current_node.add_to_payload(new_payload)
            print(current_node.payload)
            return current_node

class TreeNode:
    def __init__(self, key, payload, left_child = None, right_child = None, parent = None):
        self.key = key
        self.payload = set()
        if isinstance(payload, list):
            for element in payload:
                self.payload.add(element)
        else:
            self.payload.add(payload)
        self.left_child = left_child
        self.right_child = right_child
        self.parent = None
    
    def __repr__(self):
        return self.key
    
    def add_to_payload(self, new_payload):
        if isinstance(new_payload, list):
            for element in new_payload:
                self.payload.add(element)
        else:
            self.payload.add(new_payload)

    def is_root(self):
        if self.parent == None:
            return True
        else:
            return False
    
    def is_left_child(self):
        if self.parent and self.parent.left_child == self:
            return True
        else:
            return False

    def is_right_child(self):
        if self.parent and self.parent.right_child == self:
            return True
        else:
            return False
    
    def has_right_child(self):
        if self.right_child:
            return True
        else:
            return False
    
    def has_left_child(self):
        if self.left_child:
            return True
        else:
            return False

    def is_left(self):
        if self.right_child == None and self.left_child == None:
            return True
        else:
            return False

    def has_any_child(self):
        if self.right_child or self.left_child:
            return True
        else:
            return False
    
    def has_both_children(self):
        if self.right_child and self.left_child:
            return True
        else:
            return False

# tests

sample_bst = BST()
key_f = sample_bst.insert('f', 1)
key_a = sample_bst.insert('a', 2)
key_h = sample_bst.insert('h', 3)
key_z = sample_bst.insert('z', 4)
key_f_update = sample_bst.insert('f', 5)

    

