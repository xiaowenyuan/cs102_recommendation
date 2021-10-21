from collections import deque

debug_status = False

def debugprint(str):
    if debug_status:
        print(str)

class BST:
    def __init__(self):
        self.root = None
        self.size = 0
        self.max_depth = 0

    def get_bst_size(self):
        return self.size

    def get_tree_depth(self):
        return self.max_depth

    def put(self, new_key, new_payload):
        debugprint('\n------------------------------------------------')
        debugprint(f'\nStarting the inserting function for {new_key}')
        #check if self.root exists
        if self.root:
            #if self.root exists, run the _put function recursively
            new_node = self._put(new_key, new_payload, self.root, self.root.depth)
            return new_node
        #if self.root does not exist, make a new root
        else:
            self.root = TreeNode(new_key, new_payload, 1, None)
            self.max_depth += 1
            debugprint(f'No root exists. Creating a new node {new_key} at depth {self.root.depth}')
            self.size += 1
            return self.root
        

    def _put(self,new_key, new_payload, current_node, depth):
        debugprint(f'\nChecking node {current_node} to place new node {new_key} at depth {depth}')
        #check if new_key < current_node.key --> checking left child 
        if new_key < current_node.key:
            #check if left child exists
            if current_node.has_left_child():
                #if left_child exists run the put method recursively with left_child as the current node now
                return self._put(new_key, new_payload, current_node.left_child, current_node.depth + 1)
            else:
                #if left_child does not exist then put the key as the current node's left_child
                current_node.left_child = TreeNode(new_key, new_payload, current_node.depth + 1, current_node)
                self.size += 1
                debugprint(f'Inserting new node {new_key} to the left of {current_node} at depth {current_node.left_child.depth}')
                if self.max_depth < current_node.left_child.depth:
                    self.max_depth = current_node.left_child.depth
                return current_node.left_child
        #check if new_key > self.root.key --> checking right child
        elif new_key > current_node.key:
            #check if right child exists
            if current_node.has_right_child():
                #if right_child exists, run the put method recursively with right_child as current node
                return self._put(new_key, new_payload, current_node.right_child, current_node.depth + 1)
            else:
                #if right_child does not exist, insert the key as current node's right_child
                current_node.right_child = TreeNode(new_key, new_payload, current_node.depth + 1, current_node)
                self.size += 1
                debugprint(f'Inserting new node {new_key} to the right of {current_node} at depth {current_node.right_child.depth}')
                if self.max_depth < current_node.right_child.depth:
                    self.max_depth = current_node.right_child.depth
                return current_node.right_child
        #if new_key == current_node.key, update the key with the new payload
        else:
            debugprint(f'Updating {current_node} node\'s payload to include {new_payload}. {current_node}\'s payload is now:')
            current_node.add_to_payload(new_payload)
            debugprint(current_node.payload)
    
    def __setitem__(self, new_key, new_payload):
        self.put(new_key, new_payload)
    
    def update_from_database(self, studio_list):
        list_of_studios = studio_list.show_studios()
        for studio in list_of_studios:
            for activity in studio.activities:
                for tag in activity.tags:
                    lowertag = tag.lower()
                    self.put(lowertag, activity)

    def bft(self, search_input):
        #check if root exists. if root does not exist, return None
        if self.root:
            #implement frontier queue 
            path_queue = deque()
            initial_path = [self.root]
            path_queue.appendleft(initial_path)
            result_list = []
            #while there is still anything left in the frontier queue:
            while path_queue:
                #Pop the next path list off the frontier
                current_path = path_queue.pop()
                #Get the frontier node from the path list
                current_node = current_path[-1]
                debugprint(f'Searching node with key: {current_node.key}')
                #at each node check if key == search_input. if so, append key to possible list
                if current_node.key == search_input or search_input == current_node.key[0:len(search_input)]:
                    result_list.append(current_node)
                #for each child of the current node:
                for child in current_node.get_children():
                #make a copy of the current path
                    new_path = current_path.copy()
                #add the child to the copy
                    new_path.append(child)
                #append the updated path to the frontier queue
                    path_queue.appendleft(new_path)
            return result_list
        else:
            return None
        
    def get(self, key_search):
        debugprint('\n+++++++++++++++++++++++++++++++++++++++++++++++')
        debugprint(f'\nStarting the get function for {key_search}')
        #check if self.root exists
        if self.root:
            #if self.root exists, run the _get function
            resulting_node = self._get(key_search, self.root)
            if resulting_node:
                resulting_payload = resulting_node.payload
                debugprint(f'Returning the payload of {resulting_node}')
                return resulting_payload
            else:
                return None
        #if self.root does not exist, return None
        else:
            print('No root available.')
            return None

    def _get(self, key_search, current_node):
        #if current_node does not exist, return None
        if not current_node:
            debugprint(f'{key_search} does not exist in this tree')
            return None
        #if current_node exists
        # check current_node.key == key_search, then return the payload of the key
        elif current_node.key == key_search:
            debugprint(f'Found {key_search} at node {current_node}')
            return current_node
        #if key_search < current_node, run the function recursively on current_node.left_child
        elif key_search < current_node.key:
            debugprint(f'Searching the left child of {current_node} ({current_node.left_child}) for the key {key_search}')
            return self._get(key_search, current_node.left_child)
        #if key_search > current_node, run the function recursively on current_node.right_child
        else:
            debugprint(f'Searching the right child of {current_node} ({current_node.right_child}) for the key {key_search}')
            return self._get(key_search,current_node.right_child)
    
    #implement __getitem__
    def __getitem__(self, key_search):
        return self.get(key_search)

    #implement __contains__ which overrides in operator
    def __contains__(self, key_search):
        if self._get(key_search, self.root):
            return True
        else:
            return False

    #define delete node function
    def delete(self, key):
        debugprint(f'\nDeleting key {key}')
        #check if tree size > 1 
        if self.size > 1:
            node_to_remove = self._get(key, self.root)
            self.remove(node_to_remove)
            self.size -= 1
        #check if tree size is 1 and confirm if the key to be removed is the root
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self -= 1
        else:
            raise KeyError(f'Key {key} is not in tree')
    
    #define remove node function
    def remove(self, node_to_remove):
        #check if node has no child
        if node_to_remove.is_leaf():
            #check if node is a left child
            if node_to_remove.is_left_child():
                node_to_remove.parent.left_child = None
                debugprint(f'Node {node_to_remove.key} is a leaf node and a left child. Setting its parent {node_to_remove.parent.key}\'s left child to None')
            else:
                node_to_remove.parent.right_child = None
                debugprint(f'Node {node_to_remove.key} is a leaf node and a right child. Setting its parent {node_to_remove.parent.key}\'s right child to None')
        #check if node has two children
        elif node_to_remove.has_both_children():
            #need to find the node's successor 
            successor_node = node_to_remove.find_successor()
            debugprint(f'Node {node_to_remove.key} has two children. Replacing node {node_to_remove.key} with {successor_node.key}')
            #splice out the successor 
            successor_node.splice_out()
            #replace the node with the successor node
            node_to_remove.replace_node_data(successor_node.key, successor_node.payload, node_to_remove.left_child, node_to_remove.right_child)
        #if node has only one child
        else:
            #if node has only left child
            if node_to_remove.has_left_child():
                replacement_node = node_to_remove.left_child
                #check if node is a left child
                if node_to_remove.is_left_child():
                    #node's left child becomes parent's left child
                    node_to_remove.parent.left_child = replacement_node
                    #node's parent becomes left child's parent
                    replacement_node.parent = node_to_remove.parent
                    debugprint(f'Node {node_to_remove.key} has a left child {replacement_node.key}. Setting its parent {node_to_remove.parent}\'s left child to {replacement_node.key}')
                #check if node is a right child
                elif node_to_remove.is_right_child():
                    node_to_remove.parent.right_child = replacement_node
                    replacement_node.parent = node_to_remove.parent
                    debugprint(f'Node {node_to_remove.key} has a left child {replacement_node.key}. Setting its parent {node_to_remove.parent}\'s right child to {replacement_node.key}')
                #check if node is root (ie has no parents)
                else:
                    #replace node with child's key, payload, left child, right child
                    node_to_remove.replace_node_data(replacement_node.key, replacement_node.payload, replacement_node.left_child, replacement_node.right_child)
                    debugprint(f'Node {node_to_remove.key} is root. Replacing it with its left child {replacement_node.key}.')
            #check if node has only right child
            else:
                replacement_node = node_to_remove.right_child
                #check if node is a left child
                if node_to_remove.is_left_child():
                    #node's left child becomes parent's left child
                    node_to_remove.parent.left_child = replacement_node
                    #node's parent becomes left child's parent
                    replacement_node.parent = node_to_remove.parent
                    debugprint(f'Node {node_to_remove.key} has a right child {replacement_node.key}. Setting its parent {node_to_remove.parent}\'s left child to {replacement_node.key}')
                #check if node is a right child
                elif node_to_remove.is_right_child():
                    node_to_remove.parent.right_child = replacement_node
                    replacement_node.parent = node_to_remove.parent
                    debugprint(f'Node {node_to_remove.key} has a right child {replacement_node.key}. Setting its parent {node_to_remove.parent}\'s right child to {replacement_node.key}')
                #check if node is root (ie has no parents)
                else:
                    #replace node with child's key, payload, left child, right child
                    node_to_remove.replace_node_data(replacement_node.key, replacement_node.payload, replacement_node.left_child, replacement_node.right_child)
                    debugprint(f'Node {node_to_remove.key} is root. Replacing it with its right child {replacement_node.key}.')
    
    def depth_first_traversal(self, node = None):
        if node is None:
            node = self.root
            print('Printing inorder depth-first-traversal')
        if self.size == 1: 
            print(f'Tree only has root node of {self.root.key} at depth {self.root.depth}')
        elif self.size == 0:
            print('No tree available')
        else:
            current_node = node
            if current_node.has_left_child():
                self.depth_first_traversal(current_node.left_child)
            print(f'Depth = {current_node.depth}, Key = {current_node.key}')
            if current_node.has_right_child():
                self.depth_first_traversal(current_node.right_child)

class TreeNode:
    def __init__(self, key, payload, depth, parent, left_child = None, right_child = None):
        self.key = key
        self.payload = set()
        if isinstance(payload, list) or isinstance(payload, set):
            for element in payload:
                self.payload.add(element)
        else:
            self.payload.add(payload)
        self.depth = depth
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent
    
    def __repr__(self):
        return self.key

    def get_children(self):
        children_list = []
        if self.left_child:
            children_list.append(self.left_child)
        if self.right_child:
            children_list.append(self.right_child)
        return children_list
    
    def add_to_payload(self, new_payload):
        if isinstance(new_payload, list) or isinstance(new_payload, set):
            for element in new_payload:
                self.payload.add(element)
        else:
            self.payload.add(new_payload)

    def replace_node_data(self, key, payload, left_child, right_child):
        self.key = key
        self.payload = set()
        if isinstance(payload, list) or isinstance(payload, set):
            for element in payload:
                self.payload.add(element)
        else:
            self.payload.add(payload)
        self.left_child = left_child
        self.right_child = right_child
        if self.has_right_child():
            self.right_child.parent = self
        if self.has_left_child():
            self.left_child.parent = self
        
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

    def is_leaf(self):
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

    def find_successor(self):
        successor = None
        if self.has_right_child():
            successor = self.right_child.find_min()
        #self has no right child and there are two options: it is left child of its parent, or right child of its parent
        else:
            if self.parent:
                if self.is_left_child():
                    successor = self.parent
                else:
                    #the successor will be the successor of the parent excluding the current node, so we have to first initialise current node as None
                    self.parent.right_child = None
                    successor = self.parent.find_successor()
                    #re-initialise current node as successor has been found
                    self.parent.right_child = self
        return successor 

    def find_min(self):
        current_node = self
        #loop through all the left children
        while current_node.has_left_child():
            current_node = current_node.left_child
        return current_node

    def splice_out(self):
        #check if self is leaf node
        if self.is_leaf():
            #check if self is a left child
            if self.is_left_child():
                self.parent.left_child = None
            #check if self is a right child
            else:
                self.parent.right_child = None
        #self has child
        elif self.has_any_child():
            #self has left child
            if self.has_left_child():
                #check if self is a left child
                if self.is_left_child():
                    self.parent.left_child = self.left_child
                #check if self is a right child
                else:
                    self.parent.right_child = self.left_child
                #set the child's parent correctly to self's parent
                self.left_child.parent = self.parent
            #self has right child
            else:
                #check if self is a left child
                if self.is_left_child():
                    self.parent.left_child = self.right_child
                #check if self is a right child
                else:
                    self.parent.right_child = self.right_child
                #set child's parent accordingly
                self.right_child.parent = self.parent

# tests
if __name__ == '__main__':
    sample_bst = BST()
    key_f = sample_bst.put('f', 1)
    key_b = sample_bst.put('b', 2)
    key_h = sample_bst.put('h', 3)
    key_z = sample_bst.put('z', 4)
    key_f_update = sample_bst.put('f', 5)
    key_j = sample_bst.put('j', 6)
    key_m = sample_bst.put('m', 7)
    key_e = sample_bst.put('e', 8)
    key_e_update = sample_bst.put('e', 9)
    sample_bst['a'] = 10
    sample_bst['c'] = 11
    sample_bst['g'] = 12
    sample_bst['d'] = 13
    print('\n**************************************************')
    sample_bst.depth_first_traversal()
