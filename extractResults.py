import os
import csv
import sys
import getopt

def extractRes(out, err):
	outList = os.listdir(out)
	errList = os.listdir(err)

	# hold results as (formula,(cpu,conflicts))
	tupList = []

	# iterate over all files
	for f in errList:
		# check if also in outout
		outFile = f.replace('.err','.out')
		formula = f.replace('.err','.cnf')
		# check if matching in both dirs
		if outFile in outList:
			errFilePath = os.path.join(err,f)
			outFilePath = os.path.join(out,outFile)
			# check if timeout
			if os.stat(errFilePath).st_size != 0:
				txt = open(errFilePath, 'r').read()
				if 'exceeded limit' in txt:
					newTup = (formula,('TIMEOUT','TIMEOUT'))
					tupList.append(newTup)
			# no timeout
			else:
				# parse output file
				for line in open(outFilePath,'r').readlines():
					if 'CPU time' in line:
						cpu = line.split()[4]
					if 'c conflicts' in line:
						conflicts = line.split()[3]
				try:
					newTup = (formula,(cpu,conflicts))
					tupList.append(newTup)
				except:
					print "Error: Couldn't add file {0}".format(outFile)
					continue
	
	resDict = dict(tupList)
	
	return resDict

def main(argv):
	# path to output files
	outPath = 'output'
	# path to error files
	errPath = 'error'
	# csv file name to produce
	csvFile = 'results.csv'
	try:
		opts, args = getopt.getopt(argv, "ho:e:r:")
	except getopt.GetoptError:
		print 'extractResults.py -p <path> -t <timeout>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'extractResults.py -o <outPath> -e <errorPath> -r <resultsFileName>'
			print '-o <outPath> - Output path'
			print '-e <errorPath> - Error path'
			print '-r <resultsFileName> - Results filename'
			sys.exit()
		elif opt == '-o':
			outPath = str(arg)
		elif opt == '-e':
			errPath = str(arg)
		elif opt == '-r':
			csvFile = str(arg) + '.csv'


	outPath = os.path.join(os.getcwd(), outPath)
	errPath = os.path.join(os.getcwd(), errPath)
	csvFile = os.path.join(os.getcwd(), csvFile)
	
	with open(csvFile, 'a', 1) as csvfile:
		fieldnames = ['formula', 'runtime', 'conflicts']
		csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		csv_writer.writeheader()
		resDict = extractRes(outPath, errPath)
		for key in resDict:
			csv_writer.writerow({'formula': key, 'runtime': resDict[key][0], 'conflicts': resDict[key][1]})
		csvfile.flush()
	csvfile.close()

if __name__ == '__main__':
	main(sys.argv[1:])