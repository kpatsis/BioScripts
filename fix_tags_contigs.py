#! /usr/bin/env python
import sys
import random
from subprocess import call

fname = sys.argv[1]
fname_list = fname.split('.')
fext = fname_list.pop()
fname_pure = ""
for el in fname_list:
    fname_pure = fname_pure + el + '.'

if (fext == "fastq") or (fext == "fq"):
        awk = "awk \'BEGIN{P=1}{if(P==1||P==2){gsub(/^[@]/,\">\");print}; if(P==4)P=0; P++}\' "
        new_name = fname_pure+"fasta"
        awk = awk +  fname + " > " + new_name
        call(awk,shell=True)
        #call(["rm",sys.argv[1]])


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
