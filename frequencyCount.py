#!/usr/bin/python
import argparse
import os
import sys

class WordFrequencyCount:
	def __init__(self, memoryUsageInMegabytes, inputfilename, outputfilename):
		self.inputFileName = inputfilename
		self.outputFileName = outputfilename
		self.maxMemoryUsage = memoryUsageInMegabytes * 1024 * 1024
		self.wordArray = []

	def count(self):
		inFile = open(self.inputFileName, 'r')
		outFile = open(self.outputFileName, 'w')

		memoryUsed = 0
		currWord = None
		currCount = 0
		while(True):
			line = inFile.readline().rstrip()
			if(line == ""):
				break;
			if(line != currWord):
				if(currWord is not None):
					entry = (currWord, currCount)
					self.wordArray.append(entry)
					memoryUsed += sys.getsizeof(entry) + sys.getsizeof(currWord) + sys.getsizeof(currCount)

				if(memoryUsed > self.maxMemoryUsage):
					for word, count in self.wordArray:
						outFile.write(word + ' ' + str(count) + '\n')
					memoryUsed = 0
					self.wordArray = []

				currWord = line
				currCount = 1
			else:
				currCount += 1
			
			sys.stdout.write("\r" + str(memoryUsed))
			sys.stdout.flush()
			


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('memory',
						'<memory>',
						nargs=1,
                        help='amount of memory to use')
	parser.add_argument('inputfilename',
                        metavar='<input_filename>',
                        nargs=1,
                        help='name of input file')
	parser.add_argument('outputfilename',
                        metavar='<outputfilename>',
                        nargs=1,
                        help='name of input file')

	args = parser.parse_args()

	print args
	freqCount = WordFrequencyCount(int(args.memory[0]), args.inputfilename[0], args.outputfilename[0])
	freqCount.count()

if __name__ == '__main__':
    main()