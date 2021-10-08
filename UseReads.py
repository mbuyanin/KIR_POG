import os
from dataclasses import dataclass
import NewCreatePog
import CreatePOG
import re
import csv
import time

MSA_directory = os.listdir('/home/mbuyanin/Documents/KIR_MSA/MSA/MY_FORMAT/')

@dataclass
class reads:
    sequence : str
    actual : str
    predicted : list
    def __init__(self, sq : str, act : str, prd : list):
        self.sequence = sq
        self.actual = act
        self.predicted = prd

reads_1 = []
reads_2 = []
POGs = {}

def getReads():
    with open('Sim_100_350.read.info') as read_file:
        line_info = read_file.readline()
        while line_info.startswith('#'):
            line_info = read_file.readline()
        with open('Sim_100_350_1.fq') as simulated_file_1:
            with open('Sim_100_350_2.fq') as simulated_file_2:
                while True:
                    line_1 = simulated_file_1.readline()
                    line_1 = simulated_file_1.readline()
                    if line_1 == None or line_1 == '':
                        break
                    actual_1 = re.search('&\t(.*?)\t', line_info).group(1)
                    source_1 = re.search('.fasta\t(.*?)&', line_info).group(1)
                    gene_type_1 = find_location(source_1, actual_1)
                    reads_1.append(reads(line_1[:-1], gene_type_1, []))
                    line_1 = simulated_file_1.readline()
                    line_1 = simulated_file_1.readline()

                    line_info = read_file.readline()

                    line_2 = simulated_file_2.readline()
                    line_2 = simulated_file_2.readline()
                    actual_2 = re.search('&\t(.*?)\t', line_info).group(1)
                    source_2 = re.search('.fasta\t(.*?)&', line_info).group(1)
                    gene_type_2 = find_location(source_2, actual_2)
                    reads_2.append(reads(line_2[:-1], gene_type_2, []))
                    line_2 = simulated_file_2.readline()
                    line_2 = simulated_file_2.readline()

                    line_info = read_file.readline()

def find_location(source, position):
    new_source = '>' + source +'&'
    with open("../ResearchTools/KIRHaplotypeGenerator/outputCoordinates/output_1.txt", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        currentString = False
        gene_type = 'N/A'
        for row in csv_reader:
            if row[0] == new_source:
                currentString = True
            elif row[0].startswith(">"):
                currentString = False
            if currentString == True and not row[0].startswith(">"):
                if int(row[1]) <= int(position) and int(position) <= int(row[2]):
                    gene_type = re.search('(.*?)\*', row[0]).group(1)
    return gene_type
                    

def new_pog_OLD():
    for file in MSA_directory:
        if file.startswith('FORMAT_KIR3DP1_gen'):
            dot_location = file.find('.')
            POGs[file[7:dot_location]] = NewCreatePog.create_pog(file)

def reverse_complement(read):
    new_read = ''
    for i in range(0, len(read)):
        if read[len(read) - 1 - i] == 'A':
            new_read += 'T'
        if read[len(read) - 1 - i] == 'C':
            new_read += 'G'
        if read[len(read) - 1 - i] == 'G':
            new_read += 'C'
        if read[len(read) - 1 - i] == 'T':
            new_read == 'A'
    return new_read

def testing_reads_OLD():
    with open ('ReadResults.txt', 'w') as results:
        results.write('SEQUENCE\t\t\t\t\t\t\tACTUAL\t\t\t\tPREDICTED\n')
        for pog in POGs:
            print(pog)
            count = 0
            for read in reads_1:
                count += 1
                if count % 500 == 0:
                    print('AMOUNT COMPUTED: ' + str(count))
                #print('SOURCE: ' + read.actual + '\t\tNUM: ' + str(count) + '\tOUT OF: ' + str(len(reads_1)))
                right = False
                #if read.actual == 'KIR3DP1':
                    #print('Should work')
                    #right = True
                with open('garbage.txt', 'w') as garbage_test:
                    for i in range(0, len(POGs[pog])):
                        current_sequence = POGs[pog][i][0].sequence
                        n = 0
                        while n <= len(POGs[pog][i]) - len(read.sequence):
                            possible_sequence = True
                            current_sequence = POGs[pog][i][0].sequence
                            read_position = 0
                            pog_sequence = ''
                            read_reverse_compl = False
                            possible_read_reverse_comp = True
                            for a in range(n, len(POGs[pog][i])):
                                if right:
                                    pog_sequence += reverse_complement(read.sequence[len(read.sequence) - read_position - 1])
                                while POGs[pog][i][a].base == '-':
                                    a += 1
                                    n += 1
                                #print(read.sequence[read_position])
                                if not read_reverse_compl:
                                    if read.sequence[read_position] != POGs[pog][i][a].base:
                                        if read_position == 0 and reverse_complement(read.sequence[len(read.sequence) - read_position -1]) == POGs[pog][i][a].base:
                                            read_reverse_comp = True
                                        else:
                                            possible_sequence = False
                                            break
                                else:
                                    if reverse_complement(read.sequence[len(read.sequence) - read_position - 1]) != POGs[pog][i][a].base:
                                        possible_sequence = False
                                        break

                                read_position += 1
                                if read_position == len(read.sequence):
                                    print('yes')
                                    break
                            
                            #if right:
                                #print(pog_sequence)
                            if possible_sequence:
                                read.predicted.append(current_sequence)
                            n += 1
                    #print('done with: ' + read.actual)
                entry_string = ''
                for entry in read.predicted:
                    entry_string += entry + ', '
                results.write(read.sequence + '\t' + read.actual + '\t[' + entry_string[:-2] + ']\n')

def new_pog():
    for file in MSA_directory:
        if file.startswith('FORMAT_KIR3DP1_gen'):
            dot_location = file.find('.')
            POGs[file[7:dot_location]] = CreatePOG.create_pog(file)
            print('created')

def testing_reads():
    with open ('ReadResults.txt', 'w') as results:
        results.write('SEQUENCE\t\t\t\t\t\t\tACTUAL\t\t\t\tPREDICTED\n')
        for pog in POGs:
            print(len(POGs[pog]))
            for read in reads_1:
                checking_reads_on_pogs(POGs[pog], read)
                read.sequence = reverse_complement(read.sequence)
                checking_reads_on_pogs(POGs[pog], read)
                read.sequence = reverse_complement(read.sequence)
                entry_string = ''
                for entry in read.predicted:
                    entry_string += entry + ', '
                results.write(read.sequence + '\t' + read.actual + '\t[' + entry_string[:-2] + ']\n')
                print(entry_string)

                
                    
def checking_reads_on_pogs(pog, read):
    for i in range(0, len(pog) - len(read.sequence)):
        current_position_on_read = 0
        sequences = []
        bases = CreatePOG.getPossibleBases(pog[i])
        if 'A' in bases and 'A' == read.sequence[0]:
            sequences = pog[i].A.sequences
        elif 'C' in bases and 'C' == read.sequence[0]:
            sequences = pog[i].C.sequences
        elif 'G' in bases and 'G' == read.sequence[0]:
            sequences = pog[i].G.sequences
        elif 'T' in bases and 'T' == read.sequence[0]:
            sequences = pog[i].T.sequences
        for i in range(i, i+len(read.sequence)):
            sequences = CreatePOG.traversePog(pog, i, sequences, read.sequence[current_position_on_read])
            current_position_on_read += 1
            if not sequences:
                break # Turn into return in the future
        for seq in sequences:
            if seq not in read.predicted:
                read.predicted.append(seq)



if __name__ == '__main__':
    getReads()
    new_pog()
    start = time.time()
    testing_reads()
    print('Runetime of the testing part of the reads took: ' + str(time.time() - start))