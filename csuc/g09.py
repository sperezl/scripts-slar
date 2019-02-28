#!/usr/bin/python
import os
import sys

def _parsing_var(inputFile):
    input = open(inputFile)
    for line in input:
        if line.find("%nproc") > -1:
            broken = line.split("=")
            nproc = str(broken[1].split()[0])
    return nproc


def createInput(inputFile, nproc):
    name = str(inputFile.split(".")[0])
    output = open(name+".sh", 'w')

    print >> output, "#!/bin/bash"
    print >> output, "#SBATCH --job-name=\""+ name +"\""
    print >> output, "#SBATCH -p std"
    print >> output, "#SBATCH -e "+ name +".err"
    print >> output, "#SBATCH -o "+ name +".out"
    print >> output, "#SBATCH -n "+ nproc
    print >> output, "#SBATCH -N 1"
    print >> output, "source /prod/apps/gaussian/g09d1/bsd/g09.profile"
    print >> output, "cd $SCRATCH"
    print >> output, "g09 < $SLURM_SUBMIT_DIR/"+ inputFile +" > $SLURM_SUBMIT_DIR/"+ name +".qfi\n"

    output.close()
    return name


def submitJob(name):
    print("Input "+ name + " enviat")
    os.system("sbatch "+ name + ".sh")


def main():
    for inputFile in sys.argv[1:]:
        nproc = _parsing_var(inputFile)
        name = createInput(inputFile, nproc)
        submitJob(name)

main()
