# -*- coding: utf-8 -*-
import sys, csv ,operator

data = csv.reader(open('../data/build-commiter-info-threaded.csv'),delimiter=',')
sortedlist = sorted(data, key=operator.itemgetter(0))
sortedlist.sort(key=lambda x: int(x[0]))
#now write the sorte result into new CSV file
with open('../data/build-commiter-info-sorted2.csv', "wb") as f:
	
	for row in sortedlist:
		f.write(row[0]+ ',' + row[1] + ',' + row[2] + ',' + row[3] + '\n')