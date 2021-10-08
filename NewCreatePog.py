import os
from dataclasses import dataclass
from typing import List
from collections import defaultdict

MSA_directory = os.listdir('/home/mbuyanin/Documents/KIR_MSA/MSA/MY_FORMAT/')

@dataclass
class Node:
    base : str
    position : int
    next : defaultdict(list)
    score : int
    sequence : str
    def __init__(self, b : str, pos : int, nxt : defaultdict(list), sq : str, sc = 0):
        self.base = b
        self.position = pos
        self.next = nxt
        self.score = sc
        self.sequence = sq

@dataclass
class NodeList:
    A : Node
    C : Node
    G : Node
    T : Node
    next : 'NodeList'
    position : int
    def __init(self, pos : int, nxt : 'NodeList', a : 'Node', c : 'Node', g : 'Node', t : 'Node'):
        self.position = pos
        self.next = nxt
        self.A = a
        self.C = c
        self.G = g
        self.T = t

@dataclass
class LinkedList:
    head : NodeList
    def __init__(self, top = None):
        self.head = top

def create_pog(file):
    list_of_sequences = []
    print('FILE: ' + file)
    with open('../KIR_MSA/MSA/MY_FORMAT/' + 'FORMAT_KIR3DP1_nuc.txt', 'r') as current_MSA_file:
        count = 0
        
        for line in current_MSA_file:
            count += 1
            (name, sequence) = line.split()

            temp_position = -1
            old_node = None
            
            old_list = None
            temp_node = None
            temp_string = name + '\t'
            positions = []
            for character in sequence:
                temp_position += 1
                #print(len(list_of_nodes), temp_position)
                new_node = Node(character, temp_position, None, name)

                positions.append(new_node)

            list_of_sequences.append(positions)
        
        for entry in list_of_sequences:
            sequence_string = ''
            for i in range(0, len(entry)):
                sequence_string += entry[i].base
            with open('text.txt', 'a') as temp:
                temp.write(sequence_string + '\n')
    return list_of_sequences
