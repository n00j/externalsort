#!/usr/bin/python
import argparse
import os
import sys

import externalSort
import frequencyCount

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-m',
						'--memory',
						help='amount of memory to use in megabytes',
						default='100')
	parser.add_argument('inputfilename',
                        metavar='<input_filename>',
                        nargs=1,
                        help='name of input file')
	parser.add_argument('outputfilename',
                        metavar='<outputfilename>',
                        nargs=1,
                        help='name of input file')

	args = parser.parse_args()


	sorter = externalSort.ExternalSort(int(args.memory), args.inputfilename[0])
	sorter.sort()
	
	freqCount = frequencyCount.WordFrequencyCount(int(args.memory), args.inputfilename[0] + '.out', args.outputfilename[0])
	freqCount.count()

if __name__ == '__main__':
    main()