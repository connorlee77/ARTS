import csv
import pandas as pd 
import os
import numpy as np
from datetime import date
from datetime import datetime
import time

TOY_MERGED_FILE = '../data/mergedData/11-Apr-16.csv'
MERGED_FILES = '../data/mergedData/merged_files.csv'
TIMETABLES_DIR = '../data/data/timetable/'

def getFiles(PATH):

	csvs = []
	for file in os.listdir(PATH):
		if file[-3:] == 'csv':
			csvs.append(file)

	return csvs


def importTAPData():
	frame = pd.DataFrame.from_csv(MERGED_FILES, index_col=False, infer_datetime_format=True)

	frame['station'] = None
	return frame[['Date', 'FareProduct', 'TransitCard', 'TransactionType', 'Hour', 'Minute', 'Route', 'Departure' ,'Arrival', 'Avg Arrival Diff' ,'station']]


def importTimetable(file):
	return pd.DataFrame.from_csv(TIMETABLES_DIR + file, index_col=False, infer_datetime_format=True) 


def getTimeTables():
	files = getFiles(TIMETABLES_DIR)

	days = {
		'dx': {}, 
		'sat': {}
	}

	for file in files:
		name = file.split('_')
		timetable = importTimetable(file)
		day = name[-1][:-4]

		routeName = ''
		for route in name[1:-1]:
			
			if route == '20':
				routeName += route
				continue
			
			elif route == 'CC' or route == 'CW':
				routeName += route.lower()
				
				if routeName in days[day]:
					days[day][routeName].append(timetable)
				else:
					days[day][routeName] = [timetable]

			else:
				if route in days[day]:
					days[day][route].append(timetable)
				else:
					days[day][route] = [timetable]
	
	return days


def getSeconds(dt):

	hour = dt.hour
	minute = dt.minute 
	second = dt.second

	return (hour * 60 * 60) + (minute * 60) + second


def getTapEntryData(tap_entry):
	tap_datetime = datetime.strptime(tap_entry['Date'], '%Y-%m-%d %H:%M:%S')
	tap_abstime = getSeconds(tap_datetime)

	bus_hour = str(tap_entry['Hour'])
	bus_minute = str(tap_entry['Minute'])

	bus_departtime = datetime.strptime(bus_hour + ':' + bus_minute + ':' +'00', '%H:%M:%S')

	isWeekday = tap_datetime.weekday() < 5
	dayDenoter = 'dx' if isWeekday else 'sat' 

	route = tap_entry['Route']
	if route == '51s':
		route = '51'

	return tap_abstime, bus_departtime, dayDenoter, route


def cost(time1, time2):
	return np.square(time1 - time2)



# tapTime 			: seconds
# bus_departtime 	: a time object
# table 			: a timetable dataframe
def matchStation(tapTime, bus_departtime, route, table):
	bus_depart = datetime.strftime(bus_departtime, '%I:%M %p')

	if bus_depart[0] == '0':
		bus_depart = bus_depart.lstrip('0')

	row = table.loc[(table[table.columns[2]] == bus_depart) & (table['Route'] == int(route[:2]))]

	min_diff = 10000000000
	min_station = None

	if row.empty:
		return min_station, min_diff

	for name in row.columns[2:]:
		stationTime = row[name].iloc[0]
		
		if type(stationTime) is float:
			continue

		if stationTime[0] != '1':
			stationTime = '0' + stationTime

		t = datetime.strptime(stationTime, '%I:%M %p')
		
		abs_time = t.hour * 3600 + t.minute * 60
		
		loss = cost(tapTime, abs_time)

		if loss < min_diff:
			min_diff = loss
			min_station = name

	return min_station, min_diff
	




def predictStation():

	tapData = importTAPData()
	timetables = getTimeTables()

	for index, row in tapData.iterrows():

		tapTime, bus_departtime, day, route = getTapEntryData(row)

		min_diff = 10000000000
		min_station = None
		for table in timetables[day][route]:

			station, loss = matchStation(tapTime, bus_departtime, route, table)

			if loss < min_diff:
				min_diff = loss
				min_station = station

		

		tapData.set_value(index, 'station', min_station)
		
	tapData.to_csv(path_or_buf='output/stations.csv')


def main():
	predictStation()

if __name__ == '__main__':
	main()

