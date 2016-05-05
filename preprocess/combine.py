import sys
import csv
import os


def getFiles(PATH):

	csvs = []
	for file in os.listdir(PATH):
		if file[-3:] == 'csv':
			csvs.append(file)

	return csvs




def processFile(file, PATH, OUTPUT_PATH):

	writer = csv.writer(open(OUTPUT_PATH + '/' + 'merged_files.csv', 'wb'), delimiter=',')
	file_num = 0
	for file in files:
		reader = csv.reader(open(PATH + '/' + file, 'rb'), delimiter=',')
	
		row_num = 0	
		for curr_row in reader:

			if file_num == 0:
				writer.writerow(curr_row)	
				file_num += 1
				row_num += 1
				continue 
			
			if row_num == 0:
				row_num += 1
				continue
			
			writer.writerow(curr_row)

			row_num += 1
		


if __name__ == "__main__":
	path = '../data/mergedData'
	output = '../data/mergedData'

	files = getFiles(path)
	processFile(files, path, output)