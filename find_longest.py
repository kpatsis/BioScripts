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
	if len(sec) > max:
		max = len(sec)
		max_seq = sec

print len(max_seq)

wf = open("human_chr14.fa","w")

wf.write(max_seq)

f.close()
wf.close()

