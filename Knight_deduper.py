#!/usr/bin/env python

#Bailey Knight 25 October 202
'''The purpose of this code is to adjust the start position of SAM file then remove duplicates.
    SAM files must be sorted by position prior to running this file.
    Use samtools sort file.sam -o file_sorted.sam '''


import argparse
from argparse import RawTextHelpFormatter
import re

def get_args():
    '''argument parser for generating input in terminal. All arguments are necessary
        -f input file name
        -o output file name
        -u UMI file name
        '''
    parser = argparse.ArgumentParser(description= "A program for adjusting positions of reads in sam files base CIGAR strings.\n" 
                                     "Only takes sorted SAM files.\n"
                                     "This program only takes sorted SAM files.\n"
                                     "Use SAMtools to sort the file.\n"
                                     "Use command: samtools sort file.sam -o file_sorted.sam",
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument("-f", "--file", help="Input filename", type=str)
    parser.add_argument("-o", "--outfile", help="Output filename", type=str)
    parser.add_argument("-u", "--umi", help="Your filename with all UMIs", type=str)
    return parser.parse_args()


def check_flag(flag):
    '''Checks if flag indicates forward or reverse read using bitflag 16'''
    
    if (flag & 16)!=16:
        return 'forward'
    
    elif (flag & 16)==16:
        return 'reverse'


    

def adjust_pos_start(CIGAR, position, flag):
    '''Adjust position start position based on if it is a forward or reverse read. This utilizes the above function'''
    
    cigar_string_list = re.findall(r'(\d+)([MNDS])', CIGAR)
    #returns list in following format: [("1","S"), ("14", "M")]
    
    #total value of positions used for position adjustment
    cigar_total = 0
   
    #checks flag for 16
    forward_or_reverse = check_flag(flag)
    
    #Checks if its forward sequence and subtracts softclipping value from start position
    if forward_or_reverse == 'forward':
        if "S" in cigar_string_list[0]:
            cigar_total = int(cigar_string_list[0][0])
            return position - cigar_total
        else:
            return position
    
    #Checks if its reverse sequence and subtracts softclipping value from start position
    elif forward_or_reverse == 'reverse':
        if "S" in cigar_string_list[0]:
            cigar_string_list = cigar_string_list[1::]
        for i in range(len(cigar_string_list)):
            cigar_total +=  int(cigar_string_list[i][0])
        return position + cigar_total


    
if __name__ == "__main__":
    
    #print(adjust_pos_start("10S20M30N2D8S", 100, 0))

    #Get arguments from argparser
    args = get_args()

    #set arguments to variables
    file = args.file
    outfile = args.outfile
    umi = args.umi
    
    
    umi_set = set()

    with open(umi, 'r') as umr:
        for line in umr:
            line = line.strip()
            umi_set.add(line)

    #print(len(umi_set))
    #open all files that will be used
    with open(file, 'r') as fr, open(outfile, 'w') as fw:
        
        #setting empty name
        prev_rname =''
        dupes = 0
        unique = 0
        total = 0
        #read through all lines
        for line in fr:
                if line.startswith("@"):
                    fw.write(line)
                
                else:
                    #assign needed variables of each line. Position is calculated from line_list[5]-Cigar, line_list[3] position, line_list[4] flag (position)
                    line_list = line.strip().split()
                    #print(line_list)
                    umi = line_list[0].split(':')
                    umi = umi[-1]
                    current_rname=line_list[2]
                    strandedness = check_flag(int(line_list[1]))
                    position = adjust_pos_start(line_list[5],int(line_list[3]),int(line_list[1]))
                    #adding any non duplicate to a set
                    if umi in umi_set:
                        if prev_rname != current_rname:
                            prev_rname = current_rname
                            fw.write(line)
                            #remake the set an empty set at new chroms
                            rname_set = set()
                            rname_set.add((umi, position, strandedness, current_rname))
                            unique +=1
                        
                        #write line dependent on umi and adjusted position being in set
                        elif (umi, position, strandedness, current_rname) in rname_set: # type: ignore
                            dupes += 1
                        else:
                            rname_set.add((umi, position, strandedness, current_rname)) # type: ignore
                            fw.write(line)
                            unique +=1
                    total +=1
    
    print(f'%Duplicates: {dupes/total*100}')
    print(f'%Unique: {unique/total*100}')
    print(f'Duplicates: {dupes}')
    print(f'Unique: {unique}')
    print(f'Total: {total}')


