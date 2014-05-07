#! /usr/bin/env python
import argparse
import subprocess

class DeltaElement:
	
	def __init__(self,name,length):
		# Scaffold name
		self.name = name
		# Scaffold length
		self.length = length
		# List with scaffold alignments
		self.alignments = []
		
	def add_alignment(self,rstart,rend,qstart,qend,num_ns,num_errors,ident_perc):
		self.alignments.append([rstart,rend,qstart,qend,num_ns,num_errors,ident_perc])
		

# Parse Mummer delta file
def parse_delta(filename):
	elements = []
	
	with open(filename, 'r') as f:
		elm = None
		for l in f:
			line = l.split()
			if len(line) == 4:
				tag = l.split()
				elm = DeltaElement(tag[1],int(tag[3]))
				elements.append(elm)
			elif len(line) == 7:
				alnmt = l.split()
				identity_perc = ((elm.length-int(alnmt[5]))/float(elm.length))*100.0
				elm.add_alignment(int(alnmt[0]),int(alnmt[1]),int(alnmt[2]),
						int(alnmt[3]),int(alnmt[4])-int(alnmt[5]),int(alnmt[5]),identity_perc)
						
	return elements

# Filter list with alignments for every scaffold.
# Deletes alignments with identity ratio less than align_identity 
# and of length less than scaffold_length - length_thres
def filter_alignments(alignments, align_identity, length_thres = 10):
	# iterate every aligned scaffold
	for scaf in alignments:
		# iterate every alignment
		for align in scaf.alignments:
			align_length = align[1] - align[0] + 1
			identity_perc = ((align_length-align[5])/float(align_length))*100
			if abs(align_length - scaf.length) > length_thres or identity_perc < align_identity:
				scaf.alignments.remove(align)
				
# Filter alignment list by keeping only the best alignment for each scaffold 
def keep_best(scaf_alignments,length_perc_thres):
	# iterate each aligned scaffold
	for scaf in scaf_alignments:
		max_ident = 0.0
			
		length_check = lambda x: ((x[1] - x[0] + 1 )/float(scaf.length))*100.0 >= length_perc_thres
			
		# Keep only the alignments that satisfy the length percentage threshold
		tmp_list = []
		for align in scaf.alignments:
			if length_check(align):
				tmp_list.append(align)	
				# find maximum identity percentage			
				if align[6] >= max_ident:
					max_ident = align[6]
		
		scaf.alignments[:] = tmp_list
				
		# Keep only the alignments with the maximum identity percentage
		scaf.alignments[:] = [align for align in scaf.alignments if align[6] == max_ident]
		

def main():
	# Set up argument parser
	parser = argparse.ArgumentParser(
			description="Evaluate Scaffold/Contig accuracy.")
	parser.add_argument("scaffolds",help="Contig/Scaffold multi-fasta file",type=str)
	parser.add_argument("reference",help="Reference genome in fasta format",type=str)
	parser.add_argument("-l", "--length-threshold", help="Keep only the alignments that have a \
			aligned length percentage bigger than <length_threshold>",type=float,default=95.0)
	parser.add_argument("-q", help="Quality threshold for correct alignments",type=float,default=95.0,)
	parser.add_argument("-d","--delta", help="Use specified delta file instead of running mummer", type=str)
			
	args = parser.parse_args()
	
	if args.delta == None:
		print "Running nucmer..."
		subprocess.call(["nucmer","-maxmatch",args.reference,args.scaffolds])
	
		aligns = parse_delta("out.delta")
	else:
		aligns = parse_delta(args.delta)
		
	
	keep_best(aligns,args.length_threshold)
				
	num_scaffolds = len(aligns)
	count = 0
	length = 0
	max_length = 0
	# count correct alignments
	for scaf in aligns:
		if len(scaf.alignments) > 0:
			if scaf.alignments[0][6] >= args.q:
				count = count + 1
				length = length + scaf.length
				if max_length < scaf.length:
					max_length = scaf.length
			else:
				print scaf.name, scaf.length
				for align in scaf.alignments:
					print align
		else:
			print scaf.name, scaf.length
			for align in scaf.alignments:
					print align
				
	print "Num Scaffolds:", num_scaffolds
	print "Correct scaffolds:",count
	print "Correct %:",count/float(num_scaffolds)*100.0,"%"
	print "Max correct length:", max_length
	print "Avg correct length:", length/count
	
	#for scaf in aligns:
	#	print scaf.name, scaf.length 
	#	for align in scaf.alignments:
	#		print align

main()
				
