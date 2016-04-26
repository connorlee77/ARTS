import numpy as np 
import pandas as pd 
import os 
import matplotlib.pyplot as plt

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

def getFiles(PATH):

	csvs = []
	for file in os.listdir(PATH):
		if file[-3:] == 'csv':
			csvs.append(file)

	return csvs


def getDataFrame(path, files):

	frames = []
	for file in files:
		frame = pd.DataFrame.from_csv(path + file, index_col=False, infer_datetime_format=True)
		frames.append(frame)
	return pd.concat(frames)  


def aggregateRouteDelay(frame):
	route_costs = frame.groupby('Route').agg({'Avg Arrival Diff': np.mean})
	route_costs.plot(kind='bar',color='r', legend=False)
	plt.xlabel('Route')
	plt.ylabel('Delay (min)')
	plt.title('Mean Delay of Routes')
	plt.show()

if __name__ == "__main__":

	PATH = '../data/mergedData/'

	files = getFiles(PATH)
	df = getDataFrame(PATH, files)
	
	aggregateRouteDelay(df)
