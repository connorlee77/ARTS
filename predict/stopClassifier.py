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
	
	spectral = SpectralClustering(n_clusters=2, eigen_solver='arpack', affinity="rbf")
	fit = spectral.fit_predict(stationFrameScaled)
	stationFrame['predictedClass'] = fit
	
	print(stationFrame.index.tolist())
	labels = stationFrame.index.tolist()
	fig = plt.figure()
	plt.scatter(stationFrame['Avg Arrival Diff'],stationFrame['counts'], color = colors[fit].tolist(), s=50)
	for label, x, y in zip(labels, stationFrame['Avg Arrival Diff'],stationFrame['counts']):
		plt.annotate(
        label, fontsize = 7,
        xy = (x, y), xytext = (-10, 10),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
	plt.title('The Workhorse Bus Stops of Pasadena ARTS \n - Spectral Clustering in Two Dimensions -' )
	plt.xlabel("Average Delay in minutes")
	plt.ylabel("Logarithm of total passenger count")
	plt.savefig('station.png')
	
	print("Valuable Bus Stops: \n")
	print(stationFrame[stationFrame['predictedClass'] == 1])
	
	
	# pca visualization, not as sexy as one above
	pcaDecomp =  PCA(n_components=2)
	reduced_data = pcaDecomp.fit_transform(stationFrame)
	spectral.fit(reduced_data)
	print(reduced_data)
	h = 0.3
	x_min, x_max = reduced_data[:,0].min() - 1, reduced_data[:,0].max() + 1
	y_min, y_max = reduced_data[:,1].min() - 1, reduced_data[:,1].max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
	Z = spectral.fit_predict(np.c_[xx.ravel(), yy.ravel()])
	Z = Z.reshape(xx.shape)
	fig1 = plt.figure()
	plt.imshow(Z, interpolation='nearest',extent=(xx.min(), xx.max(), yy.min(), yy.max()), cmap=plt.cm.Paired, aspect='auto', origin='lower')
	plt.plot(reduced_data[:,0], reduced_data[:,1], 'k.', markersize=8)
	plt.title('cluster')
	plt.xlim(x_min, x_max)
	plt.ylim(y_min, y_max)
	plt.xticks(())
	plt.yticks(())
	plt.savefig("SpectralClusterStops.png")