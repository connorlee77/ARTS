import csv
import pandas as pd 
import os
import numpy as np
from datetime import date
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split

import matplotlib.pyplot as plt 

''' 
	Regressed on columns: Vehicle, Day (day of week), Route, time (convert to minutes)
	Predict: 'Avg Arrival Diff'

	Random Forest Regressor: tree max depth of 20 levels  

	RMSE: 2.78213285645
	R2: 0.166345713677
'''



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
train, test = train_test_split(data, test_size=0.3, random_state=49)



rmse_test = []
rmse_train = []
r2_test = []
r2_train = []
for x in range(10, 100, 4):

	regressor = RandomForestRegressor(random_state=0, max_depth=x, max_features='auto')

	regressor.fit(train.ix[:, train.columns != 'Avg Arrival Diff'], train['Avg Arrival Diff'])

	predictions = regressor.predict(test.ix[:, test.columns != 'Avg Arrival Diff'])
	predictions_train = regressor.predict(train.ix[:, train.columns != 'Avg Arrival Diff'])

	rmse_test.append(np.sqrt(np.mean(np.square(np.subtract(test['Avg Arrival Diff'].as_matrix(), predictions)))))
	rmse_train.append(np.sqrt(np.mean(np.square(np.subtract(train['Avg Arrival Diff'].as_matrix(), predictions_train)))))
	r2_train.append(regressor.score(train.ix[:, train.columns != 'Avg Arrival Diff'], train['Avg Arrival Diff']))
	r2_test.append(regressor.score(test.ix[:, test.columns != 'Avg Arrival Diff'], test['Avg Arrival Diff']))


rmse_train = np.array(rmse_train)
rmse_test = np.array(rmse_test)
r2_test = np.array(r2_test)
r2_train = np.array(r2_train)

plt.plot(np.arange(10, 100, 4), rmse_train, label='Train RMSE') 
plt.plot(np.arange(10, 100, 4), rmse_test, label='Test RMSE')
plt.plot(np.arange(10, 100, 4), r2_train, label='Train R2') 
plt.plot(np.arange(10, 100, 4), r2_test, label='Test R2')
plt.xlabel('Depth')
plt.legend()

plt.show()



