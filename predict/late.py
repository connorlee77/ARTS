import csv
import pandas as pd 
import os
import numpy as np
from datetime import date
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split

PATH = '../data/data/gps/'

def getFiles(PATH):

	csvs = []
	for file in os.listdir(PATH):
		if file[-3:] == 'csv':
			csvs.append(file)

	return csvs


def makeFrame(files, PATH):

	frames = []	

	file_count = 0
	for file in files:
		data = file.strip().split('_')[1]
		year = int(data[0:4])
		month = int(data[4:6])
		day = int(data[6:])

		dt = date(year, month, day)

		curr_frame = pd.DataFrame.from_csv(PATH + file, index_col=False, infer_datetime_format=True)
		curr_frame['day'] = dt.weekday()

		frames.append(curr_frame)
		

		file_count += 1
	
	return pd.concat(frames)


files = getFiles(PATH)
frames = makeFrame(files, PATH)

frames['time'] = frames['Hour'] * 60 + frames['Minute']

route = pd.get_dummies(frames['Route'])
vehicle = pd.get_dummies(frames['Vehicle'])
day = pd.get_dummies(frames['day'])



data = pd.concat([vehicle, frames['time'], route, day, frames['Avg Arrival Diff']], axis=1).fillna(0)
train, test = train_test_split(data, test_size=0.3)

regressor = RandomForestRegressor(random_state=0, max_depth=20)

regressor.fit(train.ix[:, train.columns != 'Avg Arrival Diff'], train['Avg Arrival Diff'])
predictions = regressor.predict(test.ix[:, test.columns != 'Avg Arrival Diff'])

print np.sqrt(np.mean(np.square(np.subtract(test['Avg Arrival Diff'].as_matrix(), predictions))))
print regressor.score(test.ix[:, test.columns != 'Avg Arrival Diff'], test['Avg Arrival Diff'])











