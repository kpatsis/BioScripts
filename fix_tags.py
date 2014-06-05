import sys
import random
from subprocess import call

f = open(sys.argv[1],'r')
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

call(["rm",name)
call(["mv",tmp_name,name)
