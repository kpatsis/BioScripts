#! /usr/bin/env python
import sys
from pbcore.io import FastaReader

f = FastaReader(sys.argv[1])

for seq in f:
	chr = seq
	
list = chr.sequence.split('N')

max = 0
max_seq = ""
for sec in list:
	if len(seq) > max:
		max = len(seq)
		max_seq = seq

print len(seq)

