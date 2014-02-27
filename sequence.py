#! /usr/bin/env python
import argparse
import sys
import random
import os

def parse_sequence(infile):
	""" Parse DNA sequence from file (infile) """	
	seq = ""
	for l in infile.readlines():
		if l.strip()[0] == '>':
			continue
		seq += l.strip()
	return seq
	
def complement(seq):
	compdict = {
		'A':'T',
		'T':'A',
		'C':'G',
		'G':'C'
	}
	
	return [compdict[e] for e in seq]

	
def create_read(section,emis,edel,eins):
	""" Create a read from a sequence section with error """
	# mismatch dictionary
	mmdict = {
		'A':['T','G','C'],
		'T':['A','G','C'],
		'G':['A','T','C'],
		'C':['A','T','G']
	}
	
	error_stats = {
		'emis':[],
		'edel':[],
		'eins':[]
	}
	
	read = []
	for j in range(len(section)):
		read.append(section[j])
		r = random.random()	
		if r >= 0 and r < emis:
			# mismatch error
			read.append( random.choice(mmdict[read.pop()]) )
			error_stats['emis'].append(len(read)-1)
		elif r >= emis and r < (edel + emis):
			# deletion error
			read.pop()
			error_stats['edel'].append(len(read)-1)
		elif r >= (edel + emis) and r < (eins + emis + edel):
			#insertion error
			read.append(section[j])
			error_stats['eins'].append(len(read)-1)
			
	return read, error_stats
	
	
def simulate_reads(seq, args):
	""" Simulate reads with error and write them to outfile """
	sumsize = 0.0
	count_reads = 0

	# Create numreads reads
	while count_reads < args.numreads:
		# find a random index in the sequence
		index = random.randint(0,len(seq)-1)
		# set a size for the read that follows a gaussian distribution with 
		# the specified parameters
		rsize = int(random.gauss(args.mean,args.stdev))

		is_rev_comp = random.choice([True,False])
		if is_rev_comp: # reverse complement read
			section = complement(seq[index+rsize:index:-1])
		else: # normal read 
			section = seq[index:index+rsize]
			
		read, error_stats = create_read(section, args.emis, args.edel, args.eins)
		
		# check read length
		if len(read) <	args.min or len(read) > args.max:
			continue
			
		#misstr = ''.join(repr(e) + ',' for e in error_stats['emis']).rstrip(',')			
		#insstr = ''.join(repr(e) + ',' for e in error_stats['eins']).rstrip(',')			
		#delstr = ''.join(repr(e) + ',' for e in error_stats['edel']).rstrip(',')
		misstr = ''
		insstr = ''
		delstr = ''
		print >> args.outfile , ">id{}|size{}|index{}|{}|mis{}|del{}|ins{}".format(
								count_reads,len(read),index,
								{True:"rev", False:"norm"}[is_rev_comp], 
								misstr,delstr,insstr)
		print >> args.outfile , ''.join( c for c in read)

		sumsize += len(read)
		count_reads += 1
		
	return sumsize

def main():

	# Set up argument parser
	parser = argparse.ArgumentParser(
				description="Simulation of DNA sequencing. Chops DNA into random \
				pieces and outputs a multi-FASTA file.")
	parser.add_argument(
				"infile", help="FASTA file containing the DNA sequence", 
				type=argparse.FileType('r'))
	parser.add_argument("numreads", help="Number of reads to produce", type=int)
	parser.add_argument("-min", help="Minimum read size", type=int, default=50)
	parser.add_argument("-max", help="Maximum read size", type=int)
	parser.add_argument("mean", help="Reads length mean", type=int)
	parser.add_argument("stdev", help="Reads length standard deviation", type=int)
	parser.add_argument("-eins", help="Insertion error rate in range [0.0, 1.0]", 
				type=float, default=0.12)
	parser.add_argument("-edel", help="Deletion error rate in range [0.0, 1.0]", 
				type=float, default=0.02)
	parser.add_argument("-emis", help="Mis-match error rate in range [0.0, 1.0]", 
				type=float, default=0.01)
	parser.add_argument(
				'outfile', help="Specify a file to output the reads in multi-FASTA format\
				. If a file is not specified stdin will be used instead.", nargs='?',
				type=argparse.FileType('w'), default=sys.stdout)

	args = parser.parse_args()
	
	seq = parse_sequence(args.infile)

	random.seed()
	
	sumsize = simulate_reads(seq,args)

	print "Coverage {}x".format(sumsize/len(seq))
	args.outfile.close()
	args.infile.close()


main()
