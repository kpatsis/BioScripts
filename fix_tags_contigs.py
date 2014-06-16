#! /usr/bin/env python
import sys
import random
from subprocess import call

if (sys.argv[1].split('.').pop() == "fastq") or (sys.argv[1].split('.').pop() == "fq"):
        awk = "awk \'BEGIN{P=1}{if(P==1||P==2){gsub(/^[@]/,\">\");print}; if(P==4)P=0; P++}\' "
        new_name = sys.argv[1].split('.')[0]+".fasta"
        awk = awk +  sys.argv[1] + " > " + new_name
        call(awk,shell=True)
        call(["rm",sys.argv[1]])
else:
	new_name = sys.argv[1]

f = open(new_name,'r')
wf = open(sys.argv[1]+"_fixed",'w')


for l in f:
    if l[0] == '>':
        wf.write(l.split()[0]+"\n")
    else:
        wf.write(l)

name = f.name
tmp_name = wf.name

f.close()
wf.close()

call(["rm",name])
call(["mv",tmp_name,name])
