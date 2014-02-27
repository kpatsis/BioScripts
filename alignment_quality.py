#! /usr/bin/env python
import argparse
import sys

# Create a dictionary that contains the initial index and the size difference
# (reads contain a lot of insertions) of every read
def create_maf_dict(maffile,isblasr):
	maf_dict = {}
	
	# Parse the .maf file
	line = maffile.readline()
	while line != "":
		if line[0] == 'a':
			ref = maffile.readline().split()
			index = int(ref[2])
			rlength = int(ref[3])
			rsize = int(ref[5])
			query = maffile.readline().split()
			qid = query[1]
			qlength = int(query[3])
			isrev = query[4] == '-'
			
			# blasr uses the reverse reference index for the reverse-complement
			# alignments so we have to switch it
			if isrev and isblasr:
				index = rsize - index - rlength
				
			maf_dict[qid] = (index,qlength-rlength)
			
		line = maffile.readline()
	
	return maf_dict
			

# Set up argument parser
parser = argparse.ArgumentParser(
			description="Calculate mapping quality.")
parser.add_argument("-maf", help="PBSIM's alignment file (MAF format)", 
			type=argparse.FileType('r'))
parser.add_argument("-nr", help="total number of reads", type=int, default = 120000)
parser.add_argument(
			"infile", help="Alignment file (.m4 format for BLASR, .txt for seqrun)", 
			type=argparse.FileType('r'))
parser.add_argument("-tol",help="Tolerance value", type=int, default=10)
			
args = parser.parse_args()

correct_count = 0 
count = 0

isblasr = args.infile.name.split('.').pop() == 'm4'

# If there was a maf file specified, create a dictionary with the 
# initial indexes and size differences of every read
if args.maf != None:
	mafdict = create_maf_dict(args.maf,isblasr)

correct_list = []
incorrect_list = []

# Parse input file
for line in args.infile:

	if isblasr:
	
		l = line.split()
		if args.maf != None: # PBSIM
			qid = l[0].split('/')[0]
			index, dif = mafdict[qid]
		else: # MySIM
			index = int(l[0].split('|')[2][5:])
			qid = int(l[0].split('|')[0][2:])
			ndel = int(l[0].split('|')[5][3:])
			nins = int(l[0].split('|')[6].split('/')[0][3:])	
			dif = nins-ndel	
		qstart, qend, qlen = (int(x) for x in l[5:8])
		tstart, tend, tlen = (int(x) for x in l[9:12])		
				
	else: # KC
	
		# Skip comment lines
		if line[0] == '#':
			continue
			
		l = line.split()
		if args.maf != None: # PBSIM
			qid = l[0]
			index, dif = mafdict[qid]
		else: # MySIM
			qid = int(l[0].split('|')[0][2:])
			index = int(l[0].split('|')[2][5:])			
			ndel = int(l[0].split('|')[5][3:])
			nins = int(l[0].split('|')[6].split('/')[0][3:])	
			dif = nins-ndel	
			
		if qid in correct_list:
			continue
		elif qid in incorrect_list:
			count -= 1	
			
		qstart,qend, tstart,tend, qlen,tlen = (int(x) for x in l[8:14])	
		
	#if abs(index + qstart - tstart) < args.tol:
	if abs(index + qend - dif - tend) < args.tol:
		
		#if abs(index + qstart - tstart) >= 50 and abs(index + qstart - tstart) <= 60 :
		#	print "qid:",qid
		# print qid
		# print "abs(index + qend - dif - tend)", abs(index + qend - dif - tend) 
		correct_list.append(qid)		
		correct_count +=1  
	else: 
		incorrect_list.append(qid)
			
	count += 1
	
args.infile.close()
if args.maf != None:
	args.maf.close()
	
print "num alignments: ", count
print "correct alignments: ", correct_count
print "incorrect alignments: ", count - correct_count
print "skipped: ", args.nr - count

