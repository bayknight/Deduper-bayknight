#!/bin/bash                                  
#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=bgmp               #REQUIRED: which partition to use
#SBATCH --cpus-per-task=4                 #optional: number of cpus, default is 1
#SBATCH --mem=16GB                        #optional: amount of memory, default is 4GB may need to change stuff

conda activate Deduper
file=/projects/bgmp/bailey/bioinfo/Bi624/Deduper-bayknight/C1_SE_uniqAlign_sorted.sam
output=/projects/bgmp/bailey/bioinfo/Bi624/Deduper-bayknight/Dataset_tests/Deduped_C1.sam
umi=/projects/bgmp/bailey/bioinfo/Bi624/Deduper-bayknight/STL96.txt

/usr/bin/time -v \
    python ./Knight_deduper.py -f $file -o $output -u $umi