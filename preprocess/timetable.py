import csv
import os
import sys
import re

def getFiles(PATH):

	csvs = []
	for file in os.listdir(PATH):
		if file[-3:] == 'csv':
			csvs.append(file)

	return csvs



def createHeader(rows):

	assert len(rows[0]) == len(rows[1])

	top = rows[0]
	bottom = rows[1]
	
	for i in range(len(rows[0])):
		
		topNames = top[i].strip().split('&')
		bottomNames = bottom[i].strip().split('&')

		topNames = [item.strip() for item in topNames]
		bottomNames = [item.strip() for item in bottomNames]

		topNames = filter(None, topNames)
		bottomNames = filter(None, bottomNames)


		cleanTop = ' '.join(topNames)
		cleanBot = ' '.join(bottomNames)

		if cleanTop.strip() == '':
			top[i] = cleanBot
		else:
			top[i] = cleanTop + ' & ' + cleanBot

	return top


def processFile(file):
	reader = csv.reader(open('../rawdata/timetable/' + file, 'rb'), delimiter=',')
	writer = csv.writer(open('../rawdata/timetable/cleaned/' + file, 'wb'), delimiter=',')

	i = 0
	headers = []
	for row in reader:
		
		if i < 2:
			headers.append(row)
			if i == 1:
				header = createHeader(headers)
				writer.writerow(header)
		else:
			row[0] = re.sub("[^0-9]", "", row[0])
			writer.writerow(row)

		i += 1
		

def splitFile(file):
	reader = csv.reader(open('../rawdata/timetable/cleaned/' + file, 'rb'), delimiter=',')
	writer1 = csv.writer(open('../data/data/timetable/' + '1_' + file, 'wb'), delimiter=',')
	writer2 = csv.writer(open('../data/data/timetable/' + '2_' + file, 'wb'), delimiter=',')

	i = 0
	headers = []
	index = None
	for row in reader:
		
		if i == 0:
			try:
				index = row.index('')
			except ValueError:
				index = None
			i += 1
		
		if index is not None:
			row1 = row[: index]
			row2 = row[0 : 2] + row[index + 1:]

			writer1.writerow(row1)
			writer2.writerow(row2)
		else:
			writer1.writerow(row)


		
		

		
def cleanFiles():		

	files = getFiles('../rawdata/timetable')

	for file in files:
		processFile(file)


def splitData():
	files = getFiles('../rawdata/timetable/cleaned/')	
	for file in files:
		splitFile(file)


cleanFiles()
splitData()