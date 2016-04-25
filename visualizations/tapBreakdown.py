import numpy as np 
import matplotlib
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


def tapBreakdown(frame):
	frame.TransactionType.value_counts().plot(kind='bar')
	plt.ylim(0,1200)
	plt.xlabel('Transaction Type')
	plt.ylabel('Unique instances')
	plt.title('Transaction Method')
	plt.show()

if __name__ == "__main__":

	PATH = '../data/mergedData/'

	files = getFiles(PATH)
	df = getDataFrame(PATH, files)
	
	tapBreakdown(df)
