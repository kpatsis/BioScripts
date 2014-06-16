#! /usr/bin/env python
import sys
from pbcore.io import FastaReader

f = FastaReader(sys.argv[1])

sum_bp = -1
if len(sys.argv) == 3:
	sum_bp = int(sys.argv[2])

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

# compute N(G)50/90
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
        
if sum_bp != -1:        
	rsum = 0

	for rl in lenlist:
		rsum = rsum + rl
		if rsum > sum_bp/2:
		    ng50 = rl
		    break

	rsum = 0

	for rl in lenlist:
		rsum = rsum + rl
		if rsum > sum_bp*0.9:
		    ng90 = rl
		    break
else:
	ng50,ng90 = n50,n90

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
print "NG50: ", ng50
print "NG90: ", ng90
