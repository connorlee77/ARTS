import csv
import sys
import os
import pandas as pd 


def getFiles(PATH):

	csvs = []
	for file in os.listdir(PATH):
		if file[-3:] == 'csv':
			csvs.append(file)

	return csvs


def getSameDateFiles(PATH):

	files = getFiles(PATH)

	groups = {}
	for file in files:

		name = file.strip()
		name_split = name.split('_')

		if name_split[2] == 'TAP.csv':
			groups[name] = []
		

	for file in files:

		name = file.strip()
		name_split = name.split('_')

		if name_split[2] != 'TAP.csv':
			try: 
				groups['_' + name_split[1] + '_TAP.csv'].append(name)
			except KeyError:
				continue

	return groups


def pruneMissingEntries(frame, IMPORTANT_TAP, IMPORTANT_GPS):

	labels = IMPORTANT_GPS + IMPORTANT_TAP

	state = pd.notnull(frame[labels[0]])
	for name in labels[1:]:
		state = state & pd.notnull(frame[name])

	return state


def mergeSameDateFiles(PATH, file_groups, OUTPUT_PATH, IMPORTANT_TAP, IMPORTANT_GPS):

	for tap, gps_files in file_groups.items():
		tap_frame = pd.DataFrame.from_csv(PATH + tap, index_col=False, infer_datetime_format=True)
		
		date = tap_frame.iloc[0]['Date'].split()[0]

		gps_frames = []
		for gps in gps_files:
			gps_frame = pd.DataFrame.from_csv(PATH + gps, index_col=False, infer_datetime_format=True)

			gps_frame['Departure'] =  date + ' ' + gps_frame['Departure'] 
			gps_frame['Arrival'] =  date + ' ' + gps_frame['Arrival'] 

			gps_frames.append(gps_frame)

		final_gps_frame = pd.concat(gps_frames)
		frame = pd.merge(tap_frame, final_gps_frame, left_on='BusNo', right_on='Vehicle')
		
		frame['Date'] = pd.to_datetime(frame['Date'])
		frame['Departure'] = pd.to_datetime(frame['Departure'])
		frame['Arrival'] = pd.to_datetime(frame['Arrival'])

		states = pruneMissingEntries(frame, IMPORTANT_TAP, IMPORTANT_GPS)

		merged_frame = frame[(frame['Vehicle'] == frame['BusNo']) & (frame['Date'] >= frame['Departure']) & (frame['Date'] <= frame['Arrival']) & states]

		output_filename = '_'.join(date.strip().split('/')) + '.csv'
		merged_frame.to_csv(OUTPUT_PATH + output_filename, index=False)


if __name__ == "__main__":

	PATH = '../data/data/'
	OUTPUT_PATH = '../data/mergedData/'

	IMPORTANT_TAP = ['BusNo', 'Date']
	IMPORTANT_GPS = ['Vehicle', 'Departure', 'Arrival']

	files = getSameDateFiles(PATH)
	mergeSameDateFiles(PATH, files, OUTPUT_PATH, IMPORTANT_TAP, IMPORTANT_GPS)

	