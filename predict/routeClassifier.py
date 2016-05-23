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
	PATH = '../data/mergedData'
	df = getDataFrame(PATH, "For_Jim.csv")
	routeFrame = df.groupby('Route').agg({'Avg Arrival Diff': np.mean}, 'count')
	routeCount = df.groupby('Route').agg('count')
	routeFrame['counts'] = np.log(routeCount['Route'])

	
	colors = np.array([x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk'])
	colors = np.hstack([colors] * 20)
	
	routeFrameScaled = scale(routeFrame)
	
	spectral = SpectralClustering(n_clusters=2, eigen_solver='arpack', affinity="rbf")
	fit = spectral.fit_predict(routeFrameScaled)
	routeFrame['predictedClass'] = fit
	
	print(routeFrame)
	fig = plt.figure()
	plt.scatter(routeFrame['Avg Arrival Diff'],routeFrame['counts'], color = colors[fit].tolist(), s=50)
	
	plt.title('The Workhorse Routes of Pasadena ARTS \n - Spectral Clustering in Two Dimensions -' )
	plt.xlabel("Average Delay in minutes")
	plt.ylabel("Logarithm of total passenger count")
	plt.savefig('routeCluster.png')
	
	print("Valuable Routes: \n")
	print(routeFrame[routeFrame['predictedClass'] == 0])
	
	
	# pca visualization, not as sexy as one above
	pcaDecomp =  PCA(n_components=2)
	reduced_data = pcaDecomp.fit_transform(routeFrame)
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
	plt.savefig("SpectralClusterBus.png")