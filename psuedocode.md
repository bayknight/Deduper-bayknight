Problem:
For context, the data is single end RNAseq with Universal Molecular Identifiers (UMIs). SAM files can contain duplicates resulting from PCR. These duplicates can distort molecule abundances and inflate depth of coverage resulting in incorrect conclusions being drawn dependent on the experiment. There can be natural and artificial duplicates. Natural duplicates would be when a different source molecule of the same sequence is amplified. Artificial duplicates are the amplified duplicates of the intitial molecule. To discren between these two, the experiment was run using UMIs. UMIs are indexes added to the library prior to amplification. If a duplicate read has the same UMI it is most likely an artificial duplicate. The goal of this program is to identify and remove PCR duplicates from a SAM file using their SAM column information. The information that will be used are the RNAME, POS (position), strand (in Bitwise flag). We will also need to account for soft clipping using the CIGAR string. 


Functions:


def check_UMI(UMI):
    ''' checks if UMI is recognized given an UMI dictionary. if not, toss it'''
    if UMI in dict
        return true
    else 
        return false
Example check_UMI(AAATCTG): return true

def check_flag(flag)
    '''Checks if flag indicates forward or reverse read'''
    if (flag & 16) !=16:
        return 'rev'
    if (flag & 16) ==16:
        return 'rev'
Example: strand = check_flag(16) (strand would be assigned 'rev' in this case)

def adjust_seq_start(CIGAR, POS, fwdorrev):
    ''' checks CIGAR string for soft clipping and adjusts 
        sequence start position based on this. If the read
        is forward it adjusts based on the clipping so the s needs to be
        subtracted from the POS. If reverse add MDNP and S (if on the right side) to the starting position'''

Example adust_seq_start(1S, 99, fwd); return 98


return adjusted_pos
example: adjust_seq_start(1S,99, fwd) return 98
psuedo:

sort sam file before running


make UMI dictionary from file (96)

open input SAM file and Ouput SAM file:
    for line in file loop:
        if @ write to file
        else:
        assign UMI, position, flag, and cigar strings to variables
            if check_UMI(UMI): (this checks if UMI is in dictionary using function above)
                check if rname is not equal rname(in the line not the assigned variable) to where rname should be (first pass will always be true)
                    write the line to file
                    make an empty set
                    add (concatenated UMI, and new position into a string object) to a set
                else
                    adjust_seq_start(cigar,pos) to assign new position
                    concatenate the UMI, new position, reverse or forward read into a string object
                    check if that object is in the set
                        if its not add it to the set
                        write it to the output file


close file




