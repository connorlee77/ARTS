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
	plot2 = frame.TransactionType.value_counts().plot(kind='bar')
	fig2 = plot2.get_figure()
	plt.ylim(0,1500)
	plt.xlabel('Transaction Type')
	plt.ylabel('Unique instances')
	plt.title('Transaction Method')
	fig2.savefig('vizzy2.jpg')
	
    

if __name__ == "__main__":

	PATH = '../data/mergedData/'

	files = getFiles(PATH)
	df = getDataFrame(PATH, files)
	
	aggregateRouteCost(df)
