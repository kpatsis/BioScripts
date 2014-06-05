import sys
import random
from subprocess import call

if (sys.argv[1].split('.')[1] == "fastq") or (sys.argv[1].split('.')[1] == "fq"):
        awk = "awk \'BEGIN{P=1}{if(P==1||P==2){gsub(/^[@]/,\">\");print}; if(P==4)P=0; P++}\' "
        new_name = sys.argv[1].split('.')[0]+".fasta"
        awk = awk +  sys.argv[1] + " > " + new_name
        call(awk,shell=True)
        call(["rm",sys.argv[1]])

f = open(new_name,'r')
wf = open(sys.argv[1]+"_fixed",'w')

count = 120
for l in f:
    if l[0] == '>':
        wf.write(">m120322_062918_42162_c100279482550000001523008007041205_s1_p0/" + repr(random.randint(10,99)) + "/0_" + repr(count) +"\n")
    else:
        wf.write(l)
    count = count + 1

name = f.name
tmp_name = wf.name

f.close()
wf.close()

call(["rm",name])
call(["mv",tmp_name,name])
