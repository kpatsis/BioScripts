#! /usr/bin/env python
import argparse
import sys
import os
from pbcore.io import FastaReader
import matplotlib.pyplot as plt

# Set up argument parser
parser = argparse.ArgumentParser(
                        description="Create a read length distribution graph.")
parser.add_argument(
                        "infile", help="FASTA file containing the sequence reads",
                        type=str)
parser.add_argument(
                        'outfile', help="Specify a file to output the graph\
                        . The output format is deduced by the finame extension.",
                        type=argparse.FileType('w'))

args = parser.parse_args()

f = FastaReader(infile)

lenlist = [len(r.sequence) for r in f]

plt.hist(lenlist,50)
plt.ylabel('Number of reads')
plt.xlabel('Read length (bp)')
plt.savefig(args.outfile)


args.infile.close()

