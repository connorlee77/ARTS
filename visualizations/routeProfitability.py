import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import os 

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


def aggregateRouteCost(frame):
	route_costs = frame.groupby('Route').agg({'TotalCost': np.sum})
	
	date = frame.iloc[0]['Date'].split()[0]

	route_costs.plot(kind='bar',color='r', legend=False)
	plt.xlabel('Route')
	plt.ylabel('Gross Profits ($)')
	plt.title('Total Profit of Routes on ' + date)
	plt.show()




if __name__ == "__main__":

	PATH = '../data/mergedData/'

	files = getFiles(PATH)
	df = getDataFrame(PATH, files)
	
	aggregateRouteCost(df)
