import xlrd
import csv

import sys
import os


def getFiles(PATH):

	xlsx = []
	for file in os.listdir(PATH):
		if file[-3:] == 'csv':
			xlsx.append(file)

	return xlsx




def processFile(file):
	reader = csv.reader(open('../rawdata/tap/' + file, 'rb'), delimiter=',')
	writer = csv.writer(open('../data/data/tap/' + file, 'wb'), delimiter=',')
	

	header = ['Date','FareProduct','TransitCard','PaymentType','BusNo','TransactionType','SeqNo','GrpQty','TotalCost','Bonus','Change','TotalChange','ValueLeft','RidesLeft','RenewedAdvCount', 'Status']
	writer.writerow(header)		

	row_num = 0	
	previous_row = []

	bus_no = 0
	for curr_row in reader:
		if len(curr_row) == 0:
			break
		if row_num != 0:
			if curr_row[4] != '':
				bus_no = curr_row[4]
			elif len(curr_row) == 16 and curr_row[4] == '':
				curr_row[4] = bus_no
				writer.writerow(curr_row)	

		

		
		


		row_num += 1

files = getFiles('../rawdata/tap')
for file in files:
	processFile(file)