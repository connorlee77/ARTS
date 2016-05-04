import xlrd
import csv

import sys
import os


def getFiles(PATH):

	xlsx = []
	for file in os.listdir(PATH):
		if file[-4:] == 'xlsx':
			xlsx.append(file)

	return xlsx

def convert(files):

	for file in files:
		with xlrd.open_workbook(file) as wb:
		    sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
		    with open('./data/' + file[:-4] + 'csv', 'wb') as f:
		        c = csv.writer(f)
		        for r in range(sh.nrows):

		        	if r > 4:
		        		c.writerow(sh.row_values(r))

files = getFiles('./')
convert(files)