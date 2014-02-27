#! /usr/bin/env python
import sys
from pbcore.io import FastaReader

f = FastaReader(sys.argv[1])

sum = 0
lenlist = []
more1k = 0
sumncount = 0
numscaffoldwithN = 0

for r in f:
	l = len(r.sequence)
	if l > 1000:
		more1k = more1k + 1
	ncount = r.sequence.count('N')
	sumncount = sumncount + ncount
	if ncount != 0:
		numscaffoldwithN = numscaffoldwithN + 1
	sum = sum + l
	lenlist.append(l)

avglen = sum/len(lenlist)

rsum = 0

lenlist.sort()
minlen = lenlist[0]
lenlist.reverse()
maxlen = lenlist[0]

for rl in lenlist:
    rsum = rsum + rl
    if rsum > sum/2:
        n50 = rl
        break

rsum = 0

for rl in lenlist:
    rsum = rsum + rl
    if rsum > sum*0.9:
        n90 = rl
        break

print "Sum bp: ", sum
print "Num scaffolds: ", len(lenlist)
print "Avg len: ", avglen
print "Min len: ", minlen
print "Max len: ", maxlen
print "Scaffolds > 1k: ", more1k
print "Scaffolds with Ns: ", numscaffoldwithN
print "Num Ns: ", sumncount
print "N50: ", n50
print "N90: ", n90
