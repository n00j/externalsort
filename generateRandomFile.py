#!/usr/bin/python
import random
import string
import argparse
import math
import sys

def main():
	BATCH_SIZE = 500000
	parser = argparse.ArgumentParser()
	parser.add_argument('words',
						metavar='<words>',
                        nargs=1,
                        help='number of words to generate, one word per line')
	parser.add_argument('filename',
                        metavar='<filename>',
                        nargs=1,
                        help='name of output file')
	args = parser.parse_args()

	wordCount = int(args.words[0])
	
	file = open(args.filename[0], 'w')

	progress = 0
	index = 0
	while(index < wordCount):
		wordList = None
		if(index + BATCH_SIZE <= wordCount):
			wordList = [''.join(random.sample(string.letters, 30)) + '\n' for x in range(BATCH_SIZE)]
		else:
			wordsToGenerate = wordCount - index
			wordList = [''.join(random.sample(string.letters, 30)) + '\n' for x in range(wordsToGenerate)]
		file.write(''.join(wordList))
		index = index + BATCH_SIZE

		
		new_progress = float(index) / float(wordCount) * 100.0
		if(new_progress > progress):
			progress = new_progress
			sys.stdout.write("\r" + str(progress))
			sys.stdout.flush()

	sys.stdout.write("\n")

	file.close()

if __name__ == '__main__':
    main()
