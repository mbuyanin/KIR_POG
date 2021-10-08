import os
from dataclasses import dataclass
from typing import List
from collections import defaultdict

MSA_directory = os.listdir('/home/mbuyanin/Documents/KIR_MSA/MSA/MY_FORMAT/')

@dataclass
class Node:
    base : str
    position : int
    next : list
    score : int
    sequences : list
    def __init__(self, b : str, pos : int, nxt : list, sq : list, sc = 0):
        self.base = b
        self.position = pos
        self.next = nxt
        self.score = sc
        self.sequences = sq

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

def baseToString(Node):
    return Node.base

def getPossibleBases(NodeList):
    base_list = []
    if NodeList.A != None:
        base_list.append('A')
    if NodeList.C != None:
        base_list.append('C')
    if NodeList.G != None:
        base_list.append('G')
    if NodeList.T != None:
        base_list.append('T')
    return base_list

def traversePog(list_of_nodes, i, sequences, char):
    base_list = getPossibleBases(list_of_nodes[i])
    possible_sequences = []
    if char in base_list:
        for base in base_list:
            if base == 'A' and base == char:
                for seq in list_of_nodes[i].A.sequences:
                    possible_sequences.append(seq)
            if base == 'C' and base == char:
                for seq in list_of_nodes[i].C.sequences:
                    possible_sequences.append(seq)            
            if base == 'G' and base == char:
                for seq in list_of_nodes[i].G.sequences:
                    possible_sequences.append(seq) 
            if base == 'T' and base == char:
                for seq in list_of_nodes[i].T.sequences:
                    possible_sequences.append(seq)
    combo_sequence = []
    for seq in sequences:
        if seq in possible_sequences:
            combo_sequence.append(seq)
    return combo_sequence



def create_pog(file):
    start_list = None
    list_of_nodes = []
    with open('../KIR_MSA/MSA/MY_FORMAT/' + file, 'r') as current_MSA_file:
        count = 0
        positions = []
        for line in current_MSA_file:
            count += 1
            (name, sequence) = line.split()

            temp_position = -1
            old_node = None
            old_list = None
            temp_node = None
            temp_string = name + '\t'
            for character in sequence:
                temp_position += 1
                #print(len(list_of_nodes), temp_position)
                if len(list_of_nodes) <= temp_position:
                    temp_list = NodeList(None, None, None, None, None, temp_position)
                    list_of_nodes.append(temp_list)
            
                new_node = Node(character, temp_position, [], [name])
                if character != '-': #On current character
                    if (character == 'A' or character == 'a'):
                        if list_of_nodes[temp_position].A == None: #If there is no node at this location, create one
                            list_of_nodes[temp_position].A = new_node
                        else: 
                            list_of_nodes[temp_position].A.sequences.append(name)
                    elif (character == 'C' or character == 'c'):
                        if list_of_nodes[temp_position].C == None: #If there is no node at this location, create one
                            list_of_nodes[temp_position].C = new_node
                        else: 
                            list_of_nodes[temp_position].C.sequences.append(name)
                    elif (character == 'G' or character == 'g'):
                        if list_of_nodes[temp_position].G == None: #If there is no node at this location, create one
                            list_of_nodes[temp_position].G = new_node
                        else: 
                            list_of_nodes[temp_position].G.sequences.append(name)
                    elif (character == 'T' or character == 't'):
                        if list_of_nodes[temp_position].T == None: #If there is no node at this location, create one
                            list_of_nodes[temp_position].T = new_node
                        else: 
                            list_of_nodes[temp_position].T.sequences.append(name)
                
                
                temp_string += new_node.base

                if old_list == None:
                    old_list = list_of_nodes[0]
                    start_list = LinkedList(old_list)
                    #start_list.head = old_list
                else:
                    #print(old_node.base)
                    old_base = baseToString(old_node)
                    posit = 0
                    if old_base == 'A':
                        if list_of_nodes[old_node.position].A.next != []:
                            for entry in list_of_nodes[old_node.position].A.next:
                                if entry == baseToString(new_node):
                                    if list_of_nodes[old_node.position].A.next[posit] == []:
                                        print('empty')
                                        list_of_nodes[old_node.position].A.next[posit] = new_node
                                    else:
                                        print('adding')
                                        list_of_nodes[old_node.position].A.next[posit].sequences.append(name)
                                    break
                        else:
                            list_of_nodes[old_node.position].A.next.append(new_node)
                        
                        posit += 1
                old_node = new_node
                #old_list = new_list 

        return list_of_nodes
            #print(temp_string)
        #print(start_list.head.A.sequences)
        #for node in start_list.head.A.next:
        #    print(node)
        #    for base in start_list.head.A.next[node]:
        #        print(base.base, base.sequences)

        #print(list_of_nodes)
        n = 1
        m = 150
        sequences = []
        string = 'TGTCGCTCATGGTCGTCAGCATGGCGTGTGTTGGGTTCTTCTTGCTGCAGGGGGCCTGGACACATGAGGGTGGTCAGGACAAGCCCTTCCTCTCTGCCTGGCCCAGCCCTGTGGTGTCTGAAGGAGAACATGTGGCTCTTCAGTGTCGCT'
        bases = getPossibleBases(list_of_nodes[n])
        if 'A' in bases and 'A' == string[0]:
            sequences = list_of_nodes[n].A.sequences
        if 'C' in bases and 'C' == string[0]:
            sequences = list_of_nodes[n].C.sequences
        if 'G' in bases and 'G' == string[0]:
            sequences = list_of_nodes[n].G.sequences
        if 'T' in bases and 'T' == string[0]:
            sequences = list_of_nodes[n].T.sequences
        #print(sequences)
        previous_node = None
        string_character = 0
        for i in range(n, n+m):
            sequences = traversePog(list_of_nodes, i, sequences, string[string_character])
            string_character += 1
            print(i, sequences, '\n', len(sequences))
        #print(sequences)