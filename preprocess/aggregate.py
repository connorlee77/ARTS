import csv
import sys
import os


def getFiles(PATH):

	csvs = []
	for file in os.listdir(PATH):
		if file[-3:] == 'csv':
			csvs.append(file)

	return csvs


def processFile(file, PATH, OUTPUT_PATH):
	reader = csv.reader(open(PATH + '/' + file, 'rb'), delimiter=',')
	writer = csv.writer(open(OUTPUT_PATH + '/' + file, 'wb'), delimiter=',')
	
	row_num = 0	
	previous_row = []	
	for curr_row in reader:
		if row_num == 0:
			writer.writerow(curr_row)
		elif row_num == 1:
			previous_row = curr_row
			writer.writerow(curr_row)
		elif row_num > 1:

			for i in range(4):
				if curr_row[i] == '' or curr_row[i] == ' ':
					curr_row[i] = previous_row[i]
			
			previous_row = curr_row
			writer.writerow(curr_row)

		row_num += 1


def processAll(files, PATH, OUTPUT_PATH):

	for file in files:
		processFile(file, PATH, OUTPUT_PATH)


if __name__ == "__main__":

	PATH = '../rawdata'
	OUTPUT_PATH = '../data'

	files = getFiles(PATH)
	processAll(files, PATH, OUTPUT_PATH)

	










