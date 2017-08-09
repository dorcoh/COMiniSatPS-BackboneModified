import sys
import csv
import getopt
import os

def main(argv):
	# resName
	resName = 'myCompare'
	# my results
	myRes = 'results.csv'
	# output results
	outRes = 'outRes.csv'
	try:
		opts, args = getopt.getopt(argv, "hr:m:")
	except getopt.GetoptError:
		print 'compare.py -r <resName> -m <myRes>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'compare.py -r <resName> -o <origRes> -m <myRes>'
			print '-r <resName> - file name for comparing results'
			sys.exit()
		elif opt == '-r':
			resName = str(arg)
		elif opt == '-m':
			myRes = str(arg)

	myRes = os.path.join(os.getcwd(), myRes)

	mineList = []
	# parse my
	with open(myRes, 'r', 1) as my:
		# iterable
		myReader = csv.reader(my)
		myReader.next()
		for row in myReader:
			mineList.append(row)

	# {formula: (CPU,CONFCLICTS)}
	resDict = {row[0]: (row[1],row[2]) for row in mineList}

	cpu, conflicts, count = 0,0,0
	for key in resDict:
		if resDict[key][0] != 'TIMEOUT':
			cpu += float(resDict[key][0])
			conflicts += int(resDict[key][1])
			count += 1

	cpuAvg, confAvg = float(cpu)/count , float(conflicts)/count

	print count, cpuAvg, confAvg

	file_exists = os.path.isfile(outRes)
	with open(outRes, 'a', 1) as csvfile:
		fieldnames = ['solver','solved', 'avgCpu','avgConflicts']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		if not file_exists:
			writer.writeheader()
		writer.writerow({'solver': resName, 'solved': count, 'avgCpu': "%.4f" % cpuAvg, 'avgConflicts': "%.4f" % confAvg})

if __name__ == '__main__':
	main(sys.argv[1:])