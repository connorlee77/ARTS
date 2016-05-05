import xlrd
import csv

import sys
import os

path = '../rawdata/gps/'
output = '../data/data/gps/'
def getFiles(PATH):

	xlsx = []
	for file in os.listdir(PATH):
		if file[-3:] == 'csv':
			xlsx.append(file)

	return xlsx

def convert(files):

	for file in files:
		with xlrd.open_workbook(path + file) as wb:
		    sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
		    with open(file, 'wb') as f:
		        c = csv.writer(f)
		        for r in range(sh.nrows):

		        	if r > 4:
		        		c.writerow(sh.row_values(r))


files = getFiles(path)
convert(files)