from collections import deque
from random import choice

debug_status = True

def debugprint(str):
    if debug_status:
        print(str)

#Many of the BST and TreeNode methods are guided by Ch 7.13 of Pythonds https://runestone.academy/runestone/books/published/pythonds/Trees/SearchTreeImplementation.html 
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
            self.root = TreeNode(new_key, new_payload, 1, None, 0)
            self.max_depth += 1
            debugprint(f'\nNo root exists. Creating a new node {new_key} at depth {self.root.depth}')
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
                current_node.left_child = TreeNode(new_key, new_payload, current_node.depth + 1, current_node, 0)
                self.size += 1
                debugprint(f'\nInserting new node {new_key} to the left of {current_node} at depth {current_node.left_child.depth}')
                if self.max_depth < current_node.left_child.depth:
                    self.max_depth = current_node.left_child.depth
                self.update_balance_factor_upwards(current_node)
                debugprint(f'\n=====Inserting of node {new_key} is completed=====')
                return current_node.left_child
        #check if new_key > self.root.key --> checking right child
        elif new_key > current_node.key:
            #check if right child exists
            if current_node.has_right_child():
                #if right_child exists, run the put method recursively with right_child as current node
                return self._put(new_key, new_payload, current_node.right_child, current_node.depth + 1)
            else:
                #if right_child does not exist, insert the key as current node's right_child
                current_node.right_child = TreeNode(new_key, new_payload, current_node.depth + 1, current_node, 0)
                self.size += 1
                debugprint(f'\nInserting new node {new_key} to the right of {current_node} at depth {current_node.right_child.depth}')
                if self.max_depth < current_node.right_child.depth:
                    self.max_depth = current_node.right_child.depth
                self.update_balance_factor_upwards(current_node)          
                debugprint(f'\n=====Inserting of node {new_key} is completed=====')
                return current_node.right_child
        #if new_key == current_node.key, update the key with the new payload
        else:
            debugprint(f'\nUpdating {current_node} node\'s payload to include {new_payload}. {current_node}\'s payload is now:')
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
                debugprint('\nEntering while loop as frontier queue still contains:')
                debugprint(path_queue)
                #Pop the next path list off the frontier
                current_path = path_queue.pop()
                #Get the frontier node from the path list
                current_node = current_path[-1]
                debugprint(f'\nSearching node with key: {current_node}')
                #at each node check if key == search_input. if so, append key to possible list
                if current_node.key == search_input or search_input == current_node.key[0:len(search_input)]:
                    debugprint(f'{current_node.key} is added into result')
                    result_list.append(current_node)
                if current_node.has_any_child():
                    for child in current_node.get_children():
                        if child.key[:len(search_input)] == search_input:
                            new_path = current_path.copy()
                            new_path.append(child)
                            path_queue.appendleft(new_path)
                    #if current_node.key is smaller than the search_input, then search only the right child
                    if current_node.key < search_input and current_node.has_right_child():
                        debugprint(f'\nAs {current_node.key} is smaller than {search_input}, we will search only the right child, {current_node.right_child}')
                        new_path = current_path.copy()
                        new_path.append(current_node.right_child)
                        if new_path not in path_queue:
                            path_queue.appendleft(new_path)
                    #if current_node.key is larger than the search_input, then search only the left child
                    elif current_node.key > search_input and current_node.has_left_child():
                        debugprint(f'\nAs {current_node.key} is larger than {search_input}, we will search only the left child, {current_node.left_child}')
                    #make a copy of the current path
                        new_path = current_path.copy()
                    #add the left child to the copy
                        new_path.append(current_node.left_child)
                    #append the updated path to the frontier queue
                        if new_path not in path_queue:
                            path_queue.appendleft(new_path)
            debugprint(f'Ending while loop')
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
            debugprint(f'\n{key_search} does not exist in this tree')
            return None
        #if current_node exists
        # check current_node.key == key_search, then return the payload of the key
        elif current_node.key == key_search:
            debugprint(f'Found {key_search} at node {current_node}')
            return current_node
        #if key_search < current_node, run the function recursively on current_node.left_child
        elif key_search < current_node.key:
            debugprint(f'\nSearching the left child of {current_node} ({current_node.left_child}) for the key {key_search}')
            return self._get(key_search, current_node.left_child)
        #if key_search > current_node, run the function recursively on current_node.right_child
        else:
            debugprint(f'\nSearching the right child of {current_node} ({current_node.right_child}) for the key {key_search}')
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
            #update the parent's balance factor upwards
            self.update_balance_factor_upwards(node_to_remove.parent)
        #check if node has two children
        elif node_to_remove.has_both_children():
            #need to find the node's successor 
            successor_node = node_to_remove.find_successor()
            successor_node_child = None
            successor_parent = successor_node.parent
            if successor_node.has_right_child():
                successor_node_child = successor_node.right_child
            elif successor_node.has_left_child():
                successor_node_child = successor_node.left_child
            debugprint(f'Node {node_to_remove.key} has two children. Replacing node {node_to_remove.key} with {successor_node.key}')
            #splice out the successor 
            successor_node.splice_out()
            #replace the node with the successor node
            node_to_remove.replace_node_data(successor_node.key, successor_node.payload, node_to_remove.depth, node_to_remove.parent, node_to_remove.balance_factor, node_to_remove.left_child, node_to_remove.right_child)
            #update balance factor from successor parent node and upwards
            self.update_balance_factor_upwards(successor_parent)
            if successor_node_child is not None:
                #update depth from successor node child and downwards if successor node had a child
                self.update_children_depth(successor_node_child, -1)
          
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
                    node_to_remove.replace_node_data(replacement_node.key, replacement_node.payload, node_to_remove.depth, node_to_remove.parent, node_to_remove.balance_factor, replacement_node.left_child, replacement_node.right_child)
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
                #update balance factor starting from the left child 
            self.update_balance_factor_upwards(replacement_node)
            #update depth from left child downwards 
            self.update_children_depth(replacement_node)
    
    def depth_first_traversal(self, node = None):
        if node is None:
            node = self.root
            debugprint('Printing inorder depth-first-traversal')
        if self.size == 1: 
            debugprint(f'Tree only has root node of {self.root.key} at depth {self.root.depth}')
        elif self.size == 0:
            debugprint('No tree available')
        else:
            current_node = node
            if current_node.has_left_child():
                self.depth_first_traversal(current_node.left_child)
            debug_depth = self.find_depth(current_node)
            print(f'Depth = {current_node.depth}, Key = {current_node.key}, Debug Depth = {debug_depth}')
            if current_node.has_right_child():
                self.depth_first_traversal(current_node.right_child)

    def smallest_key_node(self, node):
        current_node = node
        while current_node.left_child:
            current_node = current_node.left_child
        return current_node

    def find_depth(self, node):
        depth_count = 1
        while node.parent is not None:
            depth_count += 1
            node = node.parent
        return depth_count

    def find_height(self, root_node, reference_node):
        #debugprint(f'\nFinding height from {root_node} to {reference_node}')
        if root_node is None:
            return 0

        if root_node.is_leaf():
            return root_node.depth - reference_node.depth

        left_height = self.find_height(root_node.left_child, reference_node)
        #debugprint(f'\nHeight of left sub-branch of {root_node} is {left_height}')
        right_height = self.find_height(root_node.right_child, reference_node)
        #debugprint(f'\nHeight of right sub-branch of {root_node} is {right_height}')
        return max(left_height, right_height)

    #this balancing function is inspired by https://www.askpython.com/python/examples/balanced-binary-tree
    def is_balanced(self, root_node):
        if root_node is None:
            return True

        left_height = self.find_height(root_node.left_child, root_node)
        right_height = self.find_height(root_node.right_child, root_node)

        if abs(left_height - right_height) > 1:
            return False
        
        return True
    
    def get_balance_factor(self, root_node):
        debugprint(f'\nDetermining balance factor of {root_node}')
        if root_node is None:
            return 0 
        left_height = self.find_height(root_node.left_child, root_node)
        #debugprint(f'\nHeight of left sub-branch of {root_node} is {left_height}')
        right_height = self.find_height(root_node.right_child, root_node)
        #debugprint(f'\nHeight of right sub-branch of {root_node} is {right_height}')
        debugprint(f'\nBalance Factor of {root_node} is {right_height - left_height}')
        return right_height - left_height
    
    #balancing functions are inspired by https://algorithmtutor.com/Data-Structures/Tree/AVL-Trees/ and https://betsybaileyy.github.io/AVL_Tree/ 
    def update_balance_factor_upwards(self, node):
        debugprint(f'\nUpdating balance factor of {node}')
        current_node = node
        current_node.balance_factor = self.get_balance_factor(current_node)
        if abs(current_node.balance_factor) > 1:
            self.rebalancing(current_node)
        while current_node.parent is not None:
            debugprint('\n+++while loop starts+++')
            debugprint(f'\nUpdating balance factor of {current_node} parent {current_node.parent}')
            current_node.parent.balance_factor = self.get_balance_factor(current_node.parent)
            if abs(current_node.parent.balance_factor) > 1:
                #if the parent is unbalanced, run rebalancing function on parent
                break
            current_node = current_node.parent
            debugprint('\n+++end of this iteration of while loop+++')
        debugprint('\n+++while loop ends+++')
        if current_node.parent and abs(current_node.parent.balance_factor) > 1:
            self.rebalancing(current_node.parent)

    def rebalancing(self, node):
        debugprint(f'\n-----------------Starting rebalancing of Node {node}--------------------------')
        #if node is right heavy 
        if node.balance_factor > 1:
            #if node's right subtree is not left heavy
            if node.right_child.balance_factor > -1:
                #perform left rotation on the node
                debugprint(f'\nPerforming left rotation on Node {node}')
                self.left_rotation(node)
            #if node's right subtree is left heavy, perform left right rotation on node
            else:
                debugprint(f'\nPerforming left right rotation on Node {node}')
                self.left_right_rotation(node)
            debugprint(f'\nUpdating balance factor of node {node}, which is currently {node.balance_factor}')
            self.update_balance_factor_upwards(node)    
        #if node is left heavy
        elif node.balance_factor < -1:
            #if node's left subtree is not right heavy, perform right notation on the node
            if node.left_child.balance_factor < 1: 
                debugprint(f'\nPerforming right rotation on Node {node}')
                self.right_rotation(node)
            else:
                #if node's left subtree is right heavy, perform right left rotation on the node
                debugprint(f'\nPerforming right left rotation on Node {node}')
                self.right_left_rotation(node)
            debugprint(f'\nUpdating balance factor of node {node}, which is currently {node.balance_factor}')
            self.update_balance_factor_upwards(node)     
        else:
            debugprint(f'\nNode {node} is balanced.')
        
    def left_rotation(self, node):
        debugprint(f'\nCommencing Left Rotation on node {node} at depth {node.depth}')
        debugprint(f'\nPivot node is {node.right_child} at depth {node.right_child.depth}')
        pivot_node = node.right_child
        node.depth += 1
        pivot_node.depth -= 1
        debugprint(f'\nUpdating Node {node} right child {node.right_child} to {pivot_node.left_child}')
        node.right_child = pivot_node.left_child
        debugprint(f'\nNode {node} right child is now {node.right_child}')
        if pivot_node.left_child is not None:
            debugprint(f'\nPivot node {pivot_node} has a left child {pivot_node.left_child} at depth {pivot_node.left_child.depth}. The parent of left child should be Node {node}')
            pivot_node.left_child.parent = node
            debugprint(f'\nPivot node {pivot_node} left child {pivot_node.left_child} parent is now {pivot_node.left_child.parent}')
        debugprint(f'\nUpdating pivot node {pivot_node} left child {pivot_node.left_child} to be Node {node}')
        pivot_node.left_child = node
        debugprint(f'\nPivot node {pivot_node} left child is now {node}')
        if not node.parent:
            debugprint(f'\nAs Node {node} is root with parent = {node.parent}, setting root of tree to be pivot node {pivot_node}')
            self.root = pivot_node
        elif node == node.parent.left_child:
            debugprint(f'\nAs Node {node} is the left child of {node.parent}, we set the parent {node.parent} left child to pivot node {pivot_node}')
            node.parent.left_child = pivot_node
            debugprint(f'\nThe left child of {node.parent} is now {node.parent.left_child}')
        else:
            debugprint(f'\nAs Node {node} is the right child of {node.parent}, we set the parent {node.parent} right child to pivot node {pivot_node}')
            node.parent.right_child = pivot_node
            debugprint(f'\nThe right child of {node.parent} is now {node.parent.right_child}')
        debugprint(f'\nParent of pivot node {pivot_node} is still {pivot_node.parent} while parent of node {node} is still {node.parent}')
        debugprint(f'\nUpdating parent of pivot node {pivot_node} to be parent of node {node}, {node.parent}')
        pivot_node.parent = node.parent
        debugprint(f'\nParent of pivot node {pivot_node} is now {pivot_node.parent}')
        debugprint(f'\nParent of node {node} is still {node.parent}')
        debugprint(f'\nUpdating parent of Node {node} to be pivot node {pivot_node}')
        node.parent = pivot_node
        debugprint(f'\nParent of node {node} is now {node.parent}')
        if node.left_child: 
            debugprint(f'\nLeft child of {node} is still {node.left_child} at depth {node.left_child.depth}')
            self.update_children_depth(node.left_child, 1)
        if pivot_node.right_child:
            debugprint(f'\nRight child of {pivot_node} is still {pivot_node.right_child} at depth {pivot_node.right_child.depth}')
            self.update_children_depth(pivot_node.right_child, -1)
        debugprint(f'\nPivot node {pivot_node} is now at depth {pivot_node.depth} while node {node} is now at depth {node.depth}')

    def right_rotation(self, node):
        debugprint(f'\nCommencing Right Rotation on Node {node} at depth {node.depth}')
        debugprint(f'\nPivot node is {node.left_child} at depth {node.left_child.depth}')
        pivot_node = node.left_child
        if node.parent is None:
            debugprint(f'\nAs Node {node} is currently root, we update root to be pivot node {pivot_node}')
            self.root = pivot_node
        elif node.parent.left_child == node:
            debugprint(f'\nNode {node} parent {node.parent} left child is currently {node.parent.left_child}. It must be changed to {pivot_node}')
            node.parent.left_child = pivot_node
            debugprint(f'\nThe left child of {node.parent} is now {node.parent.left_child}')
        else:
            debugprint(f'\nNode {node} parent {node.parent} right child is currently {node.parent.right_child}. It must be changed to {pivot_node}')
            node.parent.right_child = pivot_node
            debugprint(f'\nThe right child of {node.parent} is now {node.parent.right_child}')
        debugprint(f'\nUpdating pivot node {pivot_node} parent which is currently {pivot_node.parent} to be {node.parent}')
        pivot_node.parent = node.parent
        debugprint(f'\nPivot node {pivot_node} parent is now {pivot_node.parent}')
        debugprint(f'\nUpdating Node {node} parent which is currently {node.parent} to be {pivot_node}')
        node.parent = pivot_node
        debugprint(f'\nNode {node} parent is now {node.parent}')
        debugprint(f'\nUpdating Node {node} left child which is currently {node.left_child} to be pivot node {pivot_node} right child {pivot_node.right_child} ')
        node.left_child = pivot_node.right_child 
        debugprint(f'\nNode {node} left child is now {node.left_child}')
        if node.left_child is not None:
            debugprint(f'\nUpdating node {node.left_child} parent to be node {node}. Currently the parent is {node.left_child.parent}')
            node.left_child.parent = node
            debugprint(f'\nNode {node} left child {node.left_child} parent is now {node.left_child.parent}')
        debugprint(f'\nUpdating pivot node {pivot_node} right child which is currently {pivot_node.right_child} to be Node {node}')
        pivot_node.right_child = node
        debugprint(f'\nPivot node {pivot_node} right child is now {pivot_node.right_child}')
        node.depth += 1
        pivot_node.depth -= 1
        debugprint(f'\nNode {node} is now depth {node.depth} while pivot node {pivot_node} depth is now {pivot_node.depth}')
        if node.right_child:
            debugprint(f'\nRight child of {node} is still {node.right_child} at depth {node.right_child.depth}')
            self.update_children_depth(node.right_child, 1)
        if pivot_node.left_child:
            debugprint(f'\nLeft child of {pivot_node} is still {pivot_node.left_child} at depth {pivot_node.left_child.depth}')
            self.update_children_depth(pivot_node.left_child, -1)
        
    def left_right_rotation(self,node):
        debugprint(f'\n++++++++++Commencing Left Right Rotation on Node {node} at depth {node.depth}++++++++++++++++++++')
        #start with right rotation on node right child
        self.right_rotation(node.right_child)
        #perform left rotation on node
        self.left_rotation(node)
        debugprint(f'\n++++++++++Left Right Rotation on Node {node} at depth {node.depth} completed!!!!++++++++++++++++++++')
    
    def right_left_rotation(self,node):
        debugprint(f'\n++++++++++Commencing Right Left Rotation on Node {node} at depth {node.depth}++++++++++++++++++++')
        #perform left rotation on left child of node 
        self.left_rotation(node.left_child)
        #perform right rotation on node
        self.right_rotation(node)
        debugprint(f'\n++++++++++Right Left Rotation on Node {node} at depth {node.depth} completed!!!!!++++++++++++++++++++')

    def update_children_depth(self, node, n):
        #this function should update the depth of a node's children plus or minus n 
        debugprint(f'\nChanging the depth of node {node} by {n}')
        node.depth += n 
        debugprint(f'\nDepth of node {node} is now {node.depth}')
        if node.left_child:
            self.update_children_depth(node.left_child, n)
        if node.right_child:
            self.update_children_depth(node.right_child, n)

        

class TreeNode:
    def __init__(self, key, payload, depth, parent, balance_factor, left_child = None, right_child = None):
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
        self.balance_factor = balance_factor
    
    def __repr__(self):
        return str(self.key)

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

    def replace_node_data(self, key, payload, depth, parent, balance_factor, left_child, right_child):
        self.key = key
        self.payload = payload
        self.depth = depth
        self.parent = parent
        self.balance_factor = balance_factor 
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
    # sample_bst = BST()
    # key_f = sample_bst.put('f', 1)
    # key_b = sample_bst.put('b', 2)
    # key_h = sample_bst.put('h', 3)
    # key_z = sample_bst.put('z', 4)
    # key_f_update = sample_bst.put('f', 5)
    # key_j = sample_bst.put('j', 6)
    # key_m = sample_bst.put('m', 7)
    # key_e = sample_bst.put('e', 8)
    # key_e_update = sample_bst.put('e', 9)
    # sample_bst['a'] = 10
    # sample_bst['c'] = 11
    # sample_bst['g'] = 12
    # sample_bst['d'] = 13
    #sample_bst.depth_first_traversal()
    # unbalanced_tree = BST()
    # unbalanced_tree['b'] = 1
    # unbalanced_tree['a'] = 2
    # unbalanced_tree['e'] = 3
    # unbalanced_tree['c'] = 4
    # nodej = unbalanced_tree.put('j', 5)
    # unbalanced_tree['f'] = 6
    # unbalanced_tree['d'] = 7
    # unbalanced_tree['p'] = 8
    # unbalanced_tree['t'] = 9
    # unbalanced_tree['z'] = 10
    # unbalanced_tree.depth_first_traversal()
    # balanced_tree = BST()
    # balanced_tree['c'] = 1
    # balanced_tree['b'] = 2
    # balanced_tree['e'] = 3
    # balanced_tree['a'] = 3
    # balanced_tree['d'] = 3
    
    # rltree = BST()
    # node_t = rltree.put('t', 1)
    # node_p = rltree.put('p', 1)
    # node_m = rltree.put('m', 1)
    # rltree['z'] = 1
    # rltree['q'] = 1
    # rltree['k'] = 1
    # rltree['n'] = 1
    # rltree['j'] = 1

    # left_right_tree = BST()
    # node_h = left_right_tree.put('H', 1)
    # node_r = left_right_tree.put('R', 1)
    # left_right_tree['A'] = 1
    # left_right_tree['P'] = 1
    # left_right_tree['T'] = 1
    # left_right_tree['O'] = 1
    # left_right_tree['Q'] = 1
    # left_right_tree['K'] = 1
    # left_right_tree.depth_first_traversal()


    # right_left_tree = BST()
    # node_o = right_left_tree.put('O', 1)
    # right_left_tree['D'] = 1
    # right_left_tree['Z'] = 1
    # right_left_tree['F'] = 1
    # right_left_tree['B'] = 1
    # right_left_tree['H'] = 1
    # right_left_tree['K'] = 1
    # right_left_tree.depth_first_traversal()

    # right_left_tree.remove(node_o)

    # rr_simple = BST()
    # rr_simple['C'] = 1
    # rr_simple['B'] = 1
    # rr_simple['A'] = 1
    # rr_simple.depth_first_traversal()

    # lltree = BST()
    # lltree['c'] = 1
    # lltree['b'] = 1
    # dnode = lltree.put('d', 2)
    # lltree['e'] = 1
    # lltree['f'] = 1
    
    # lltree_2 = BST()
    # lltree_2['p'] = 1
    # j_node = lltree_2.put('j', 2)
    # lltree_2['t'] = 1
    # lltree_2['z'] = 1
    # lltree_2['f'] = 1
    # l_node = lltree_2.put('l', 2)
    # lltree_2['k'] = 1
    # lltree_2['m'] = 1
    # lltree_2['o'] = 1
    # lltree_2.depth_first_traversal()

    # simple_lr = BST()
    # simple_lr['a'] = 1
    # simple_lr['c'] = 1
    # simple_lr['b'] = 1

    # simple_rl = BST()
    # simple_rl['c'] = 1
    # simple_rl['a'] = 1
    # simple_rl['b'] = 1

    random_tree = BST()
    random_list = [i for i in range(1,200)]
    for n in random_list: 
        random_number = choice(random_list)
        new_node = random_tree.put(random_number, 1)
        random_list = [i for i in random_list if i is not random_number]

    print(random_tree.root)
    random_tree.remove(random_tree.root)