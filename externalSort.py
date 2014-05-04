#!/usr/bin/python
import argparse
import os

class SplitFile:
	def __init__(self, fileName, blockSize):
		self.fileName = fileName
		self.blockSize = blockSize
		self.blockFileNames = []

	def split(self):
		file = open(self.fileName, 'r')
		fileIndex = 0

		while(True):
			lines = file.readlines(self.blockSize)
			if(lines == []):
				break;
			lines.sort()
			self.writeFile(lines, fileIndex)
			fileIndex = fileIndex + 1

	def writeFile(self, data, fileIndex):
		filename = 'tmpfile_' + str(fileIndex) + '.txt'
		file = open(filename, 'w')
		file.write(''.join(data))
		file.close()
		self.blockFileNames.append(filename)

	def getFileNames(self):
		print self.blockFileNames
		return self.blockFileNames

	def cleanUp(self):
		[os.remove(f) for f in self.blockFileNames]

class MergeFiles:
	def __init__(self, fileName, fileList):
		self.fileList = fileList
		self.fileName = fileName
		self.numFiles = len(fileList)
		self.numBuffers = self.numFiles

	def merge(self):
		# 1. Open buffers to all the files
		# 2. Do an Nway merge. Assuming the files have been sorted
		outputfile = open(self.fileName + '.out', 'w')
		buffers = [None for x in range(self.numBuffers)]
		bufferFileHandles = [None for x in range(self.numFiles)]

		index = 0
		while(True):
			if(index < self.numFiles):
				bufferFileHandles[index] = open(self.fileList[index], 'r')
				buffers[index] = bufferFileHandles[index].readline()
			else:
				break;
			index += 1

		while(True):
			index = self.selectMinBuffer(buffers)
			if(index == -1):
				break
			outputfile.write(buffers[index]);
			buffers[index] = None;
			line = bufferFileHandles[index].readline();
			if(line != ""):
				buffers[index] = line
		
		for i in range(self.numFiles):
			bufferFileHandles[index].close()

	def selectMinBuffer(self, buffers):
		minBufferIndex = -1
		minStr = None

		for i in range(len(buffers)):
			if buffers[i] is not None and (minStr is None or buffers[i] < minStr):
				minBufferIndex = i
				minStr = buffers[i]

		return minBufferIndex

class ExternalSort:
	def __init__(self, memoryInMegabytes, fileName):
		self.blockSize = memoryInMegabytes * 1024 * 1024
		self.fileName = fileName

	def sort(self):
		numberOfBlocks = self.getNumberOfBlocks()

		fileSplitter = SplitFile(self.fileName, self.blockSize)
		fileSplitter.split()

		merger = MergeFiles(self.fileName, fileSplitter.getFileNames())
		merger.merge()

		fileSplitter.cleanUp()

	def getNumberOfBlocks(self):
		return os.stat(self.fileName).st_size / self.blockSize + 1 

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('memory',
						'<memory>',
						nargs=1,
                        help='amount of memory to use')
	parser.add_argument('filename',
                        metavar='<filename>',
                        nargs=1,
                        help='name of file to sort')

	args = parser.parse_args()

	sorter = ExternalSort(int(args.memory[0]), args.filename[0])
	sorter.sort()

if __name__ == '__main__':
    main()

