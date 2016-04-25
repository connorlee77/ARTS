import numpy as np 
import matplotlib
matplotlib.use('Agg')
import pandas as pd 
import os 
import matplotlib.pyplot as plt

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
	plot = route_costs.plot(kind='bar',color='r', legend=False)
	fig1 = plot.get_figure()
	plt.xlabel('Route')
	plt.ylabel('Revenue ($)')
	plt.title('Total Revenue of Routes')
	fig1.savefig('vizzy1.jpg')
	
	plot2 = frame.TransactionType.value_counts().plot(kind='bar')
	fig2 = plot2.get_figure()
	plt.xlabel('Transaction Type')
	plt.ylabel('Number of instances')
	plt.title('Transaction Methods')
	fig2.savefig('vizzy2.jpg')
    

if __name__ == "__main__":

	PATH = '../data/mergedData/'

	files = getFiles(PATH)
	df = getDataFrame(PATH, files)
	
	aggregateRouteCost(df)
