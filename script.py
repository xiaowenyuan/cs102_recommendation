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
        self.size = 0 

    def get_bst_size(self):
        return self.size

    def put(self, new_key, new_payload):
        print('\n------------------------------------------------')
        print(f'\nStarting the inserting function for {new_key}')
        #check if self.root exists
        if self.root:
            #if self.root exists, run the _put function recursively
            self._put(new_key, new_payload, self.root)
        #if self.root does not exist, make a new root
        else:
            self.root = TreeNode(new_key, new_payload)
            print(f'No root exists. Creating a new node {new_key}')
        self.size+=1 

    def _put(self,new_key, new_payload, current_node):
        print(f'\nChecking node {current_node} to place new node {new_key}')
        #check if new_key < current_node.key --> checking left child 
        if new_key < current_node.key:
            #check if left child exists
            if current_node.has_left_child():
                #if left_child exists run the put method recursively with left_child as the current node now
                self._put(new_key, new_payload, current_node.left_child)
            else:
                #if left_child does not exist then put the key as the current node's left_child
                current_node.left_child = TreeNode(new_key, new_payload)
                print(f'Inserting new node {new_key} to the left of {current_node}')
        #check if new_key > self.root.key --> checking right child
        elif new_key > current_node.key:
            #check if right child exists
            if current_node.has_right_child():
                #if right_child exists, run the put method recursively with right_child as current node
                self._put(new_key, new_payload, current_node.right_child)
            else:
                #if right_child does not exist, insert the key as current node's right_child
                current_node.right_child = TreeNode(new_key, new_payload)
                print(f'Inserting new node {new_key} to the right of {current_node}')
        #if new_key == current_node.key, update the key with the new payload
        else:
            print(f'Updating {current_node} node\'s payload to include {new_payload}. {current_node}\'s payload is now:')
            current_node.add_to_payload(new_payload)
            print(current_node.payload)
    
    def __setitem__(self, new_key, new_payload):
        self.put(new_key, new_payload)

    def get(self, key_search):
        print('\n+++++++++++++++++++++++++++++++++++++++++++++++')
        print(f'\nStarting the get function for {key_search}')
        #check if self.root exists
        if self.root:
            #if self.root exists, run the _get function
            resulting_node = self._get(key_search, self.root)
            if resulting_node:
                resulting_payload = resulting_node.payload
                print(f'Returning the payload of {resulting_node}')
                return resulting_payload
            else:
                return None
        #if self.root does not exist, return None
        else:
            return None

    def _get(self, key_search, current_node):
        #if current_node does not exist, return None
        if not current_node:
            print(f'{key_search} does not exist in this tree')
            return None
        #if current_node exists
        # check current_node.key == key_search, then return the payload of the key
        elif current_node.key == key_search:
            print(f'Found {key_search} at node {current_node}')
            return current_node
        #if key_search < current_node, run the function recursively on current_node.left_child
        elif key_search < current_node.key:
            print(f'Searching the left child of {current_node} ({current_node.left_child}) for the key {key_search}')
            return self._get(key_search, current_node.left_child)
        #if key_search > current_node, run the function recursively on current_node.right_child
        else:
            print(f'Searching the right child of {current_node} ({current_node.right_child}) for the key {key_search}')
            return self._get(key_search,current_node.right_child)
    
    #implement __getitem__
    def __getitem__(self, key_search):
        return self.get(key_search)

    #implement __contains__ which overrides in operator
    def __contains__(self, key_search):
        if self.__getitem__(key_search):
            return True
        else:
            return False

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
key_f = sample_bst.put('f', 1)
key_a = sample_bst.put('a', 2)
key_h = sample_bst.put('h', 3)
key_z = sample_bst.put('z', 4)
key_f_update = sample_bst.put('f', 5)
key_j = sample_bst.put('j', 6)
key_m = sample_bst.put('m', 7)
key_e = sample_bst.put('e', 8)
key_e_update = sample_bst.put('e', 9)
sample_bst['o'] = 10
print(sample_bst['a'])
print(sample_bst.get('k'))
if 'e' in sample_bst:
    print('Found!')
