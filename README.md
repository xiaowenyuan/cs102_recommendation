## Introduction 

Codecademy wants us to create a "basic recommendation program" using Python for the Portfolio Project in Codecademy's CS102: Data Structures and Algorithms. The program must contain the following features:

>Implementing an autocomplete that, based on a user’s input, returns a list of possible categories based on the beginning of a word. You should use the data created in the last step to create the autocomplete. It is up to you how to properly store and retrieve the data.

>Retrieving and displaying all of the data related to the category selected by the user. It is up to you how to properly store and retrieve the data.

This is a Python terminal program that recommends workout classes to a user depending on the type of workouts the user wants to do and what time they are free. 

## Running the Program 

First, run `studios.py`. This will randomly generate random studios and classes which will be inserted into a binary search tree (BST). The resulting tree is pickled, ready for the next step.

Next, run `script.py`. The program will prompt for both the activities the user is looking for, and the timing for said classes. The program's final payload is a list of classes from the database (if any) that satisfy the user's above conditions.  

## The Database 

Each time `studios.py` is run, random classes will be generated for 22 fictional studios. The studios already have a set of possible classes and the associated tags for said classes. Each class's timing, price, and instructor, however, is randomly generated each time. 

I used [Fake Address Generator](https://www.fakeaddressgenerator.com/World_Address/popular_city/city/New%20York) to generate the addresses for the studios. [Fossbytes](https://fossbytes.com/tools/random-name-generator) was also used to generate 500 random names for the instructors.

## The Data Structure 

A self-balancing Binary Search Tree is used to store the unique tags from the generated classes. Each tag is a node on the tree containing as payload a list of all the classes that have this tag. 

This BST is self-implemented for the purpose of practice. As many of the methods in this tree differ from the BST taught by Codecademy, I am incredibly grateful to online resources such as [Runestone Academy](https://runestone.academy/runestone/books/published/pythonds/Trees/SearchTreeImplementation.html) and [Algorithm Tutor](https://algorithmtutor.com/Data-Structures/Tree/AVL-Trees/) that help me implement them.

## Searching the Data Structure

Initially, a breadth-first search was employed to look for keys that contain the search term. This resulted in a linear complexity of `O(n)`, where n is the number of tags in the data structure. 

The program uses an "autocomplete" search function that should run faster as it takes advantage of the BST property. The search function has the following parts:

1. Look for the smallest term that is greater than or equal to the search term. 

2. Traverse the tree for the next largest key until the search term no longer matches the relevant part of the search term (ie `node.key[:len(search_term)]`). 

3. Return the list of nodes that contain these keys. 

This search function should have a complexity of `O(log(n) + t)`, where `n` is the number of nodes in the tree and `t` is the number of nodes that contain the search term. 
