import csv

if __name__ == '__main__':
	newFormulas = []
	with open('oh.csv', 'rb', 1) as csvfile:
		reader = csv.reader(csvfile)
		reader.next()
		for row in reader:
			if row[1] != 'TIMEOUT':
				newFormulas.append(row[0])

	f = open('2015.csv', 'w')
	s = ''
	for form in newFormulas:
		s += str(form) + '\n'
	f.write(s)
	f.close()

		