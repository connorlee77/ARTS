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

	
	colors = np.array([x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk'])
	colors = np.hstack([colors] * 20)
	
	stationFrameScaled = scale(stationFrame)
	print(stationFrame)
	
	spectral = SpectralClustering(n_clusters=2, eigen_solver='arpack', affinity="rbf")
	fit = spectral.fit_predict(stationFrameScaled)
	stationFrame['predictedClass'] = fit
	
	print(stationFrame)
	fig = plt.figure()
	plt.scatter(stationFrame['Avg Arrival Diff'],stationFrame['counts'], color = colors[fit].tolist(), s=10)
	
	plt.title('The Workhorse Bus Stops of Pasadena ARTS \n - Spectral Clustering in Two Dimensions -' )
	plt.xlabel("Average Delay in minutes")
	plt.ylabel("Logarithm of total passenger count")
	plt.savefig('station.png')
	
	h = 0.5
	x_min, x_max = stationFrame['Avg Arrival Diff'].min() - 1, stationFrame['Avg Arrival Diff'].max() + 1
	y_min, y_max = stationFrame['counts'].min() - 1, stationFrame['counts'].max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
	
	
	Z = spectral.fit_predict(np.c_[xx.ravel(), yy.ravel()])
	Z = Z.reshape(xx.shape)
	fig1 = plt.figure()
	plt.imshow(Z, interpolation='nearest',extent=(xx.min(), xx.max(), yy.min(), yy.max()), cmap=plt.cm.Paired, aspect='auto', origin='lower')
	plt.plot(stationFrame['Avg Arrival Diff'], stationFrame['counts'], 'k.', markersize=2)
	plt.title('cluster')
	plt.xlim(x_min, x_max)
	plt.ylim(y_min, y_max)
	plt.xticks(())
	plt.yticks(())
	plt.savefig("SpectralClusterStops.png")