import sys
import csv
import getopt
import os

from matplotlib import pyplot as plt

def main(argv):
	# resName
	resName = 'myCompare'
	# original results
	origRes = 'ohResults.csv'
	# my results
	myRes = 'results.csv'
	try:
		opts, args = getopt.getopt(argv, "hr:o:m:")
	except getopt.GetoptError:
		print 'compare.py -r <resName> -o <origRes> -m <myRes>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'compare.py -r <resName> -o <origRes> -m <myRes>'
			print '-r <resName> - file name for comparing results'
			print '-o <origRes> - Path for original results'
			print '-m <myRes> - Path for my results'
			sys.exit()
		elif opt == '-r':
			resName = str(arg)
		elif opt == '-o':
			origRes = str(arg)
		elif opt == '-m':
			myRes = str(arg)

	origRes = os.path.join(os.getcwd(), origRes)
	myRes = os.path.join(os.getcwd(), myRes)
	
	# parse orig
	origList =[]
	with open(origRes, 'r', 1) as orig:
		# iterable
		origReader = csv.reader(orig)
		origReader.next()
		for row in origReader:
			origList.append(row)

	mineList = []
	# parse my
	with open(myRes, 'r', 1) as my:
		# iterable
		myReader = csv.reader(my)
		myReader.next()
		for row in myReader:
			mineList.append(row)

	# {formula: (CPU,CONFCLICTS)}
	origDict = {row[0]: (row[1],row[2]) for row in origList}
	mineDict = {row[0]: (row[1],row[2]) for row in mineList}

	# create dict with key as formulas and value=(origCPU,myCPU)
	merged = dict.fromkeys(origDict.keys(),None)
	x, y = [], []
	timeOrig, timeMine = 0, 0
	confOrig, confMine = 0, 0
	timeOuts = 0

	for key in merged:
		if mineDict[key][0] != 'TIMEOUT':
			merged[key] = (origDict[key][0],mineDict[key][0])
			x.append(origDict[key][0])
			y.append(mineDict[key][0])
			timeOrig += float(origDict[key][0])
			timeMine += float(mineDict[key][0])
			confOrig += int(origDict[key][1])
			confMine += int(mineDict[key][1])
		else:
			timeOuts += 1
	
	totalSolved = len(mineDict)-timeOuts

	origAvgCPU = float(timeOrig) / len(origDict)
	mineAvgCPU = float(timeMine) / (len(mineDict)-timeOuts)
	origAvgConf = float(confOrig) / len(origDict)
	myAvgConf = float(confMine) / (len(mineDict) - timeOuts)

	fig = plt.figure()
	plt.scatter(x,y)
	titleA = 'origTotal: {0}, myTotal: {1}'.format(len(origDict), totalSolved)
	titleB = 'origAvgCPU {0}, myAvgCPU: {1}'.format(origAvgCPU, mineAvgCPU)
	titleC = 'origAvgConflicts:{0} myAvgConflicts:{1}'.format(origAvgConf, myAvgConf)
	fig.suptitle(resName + '\n' + titleA + '\n' + titleB + '\n' + titleC, fontsize=8)
	plt.xlabel('original CPU time')
	plt.ylabel('my CPU time')
	plt.xlim(0,1000)
	plt.ylim(0,1000)
	plt.savefig(resName + '.jpg')

if __name__ == '__main__':
	main(sys.argv[1:])