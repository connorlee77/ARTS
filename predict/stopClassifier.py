from time import time
import numpy as np 
import matplotlib
import pandas as pd 
import os 
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.cluster import SpectralClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale


def getDataFrame(path, filename):
    os.chdir(path)
    frame = pd.DataFrame.from_csv(filename, index_col=False, infer_datetime_format=True)
    return frame
    


if __name__ == "__main__":
	PATH = '../predict/output'
	df = getDataFrame(PATH, "stations.csv")
	stationFrame = df.groupby('station').agg({'Avg Arrival Diff': np.mean}, 'count')
	stationCount = df.groupby('station').agg('count')
	stationFrame['counts'] = np.log(stationCount['station'])
	print(stationFrame)
	
	colors = np.array([x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk'])
	colors = np.hstack([colors] * 20)

	
	spectral = SpectralClustering(n_clusters=2, eigen_solver='arpack', affinity="rbf")
	X = pd.concat([stationFrame['Avg Arrival Diff'], stationFrame['counts']])
	fit = spectral.fit_predict(stationFrame)
	stationFrame['predictedClass'] = fit
	
	print(stationFrame)
	fig = plt.figure()
	plt.scatter(stationFrame['Avg Arrival Diff'],stationFrame['counts'], color = colors[fit].tolist(), s=10)
	
	plt.title('The Workhorse Bustops of Pasadena ARTS \n - Spectral Clustering in Two Dimensions-' )
	plt.xlabel("Average Delay in minutes")
	plt.ylabel("Logarithm of total passenger count")
	plt.savefig('station.png')   