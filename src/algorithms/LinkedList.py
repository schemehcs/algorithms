import unittest
import random

class Node:
    def __init__(self, key):
        self.key = key
        self.next = None

    def __repr__(self):
        return "Node: {}".format(self.key)


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head == None

    def append(self, v):
        if self.tail == None:
            self.head = self.tail = Node(v)
        else:
            n = Node(v)
            self.tail.next = n
            self.tail = n

    def pop_left(self):
        if self.head == None:
            return None
        n = self.head
        self.head = self.head.next
        if self.head == None:
            self.tail = None
        return n.key

    def search(self, v):
        n = self.head
        while n:
            if n.key == v:
                return n
            else:
                n = n.next
        return None

