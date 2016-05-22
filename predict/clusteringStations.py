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
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

np.random.seed(187) # Ride or die mothafuckas

def getDataFrame(path, filename):
    os.chdir(path)
    frame = pd.DataFrame.from_csv(filename, index_col=False, infer_datetime_format=True)
    return frame

PATH = '../predict/output/'
df = getDataFrame(PATH, "stations.csv")
fareDummies = pd.get_dummies(df['FareProduct'], dummy_na=True)
transactionDummies = pd.get_dummies(df['TransactionType'], dummy_na=True)
routeDummies = pd.get_dummies(df['Route'],dummy_na=True)
df = pd.concat([df, fareDummies, transactionDummies, routeDummies], axis=1)

n_samples, n_features = df.shape
n_stations = len(np.unique(df.station))
labels = df.station

sample_size = 300
df = df.drop(['station'], axis = 1)
df = df.drop(['Date','FareProduct', 'TransactionType', 'Departure', 'Arrival', 'Route'], axis = 1)


df = scale(df)


print("n_digits: %d, \t n_samples %d, \t n_features %d"
      % (n_stations, n_samples, n_features))


print(79 * '_')
print('% 9s' % 'init'
      '    time  inertia    homo   compl  v-meas     ARI AMI  silhouette')


def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('% 9s   %.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f    %.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
             metrics.silhouette_score(df, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))

bench_k_means(KMeans(init='k-means++', n_clusters=n_stations, n_init=10),
              name="k-means++", data=df)

bench_k_means(KMeans(init='random', n_clusters=n_stations, n_init=10),
              name="random", data=df)

# in this case the seeding of the centers is deterministic, hence we run the
# kmeans algorithm only once with n_init=1
pca = PCA(n_components=n_stations).fit(df)
bench_k_means(KMeans(init=pca.components_, n_clusters=n_stations, n_init=1),
              name="PCA-based",
              data=df)
print(79 * '_')

# Visualize the results on PCA-reduced data
pcaDecomp =  PCA(n_components=2)
reduced_data = pcaDecomp.fit_transform(df)
kmeans = KMeans(init='k-means++', n_clusters=n_stations, n_init=10)
kmeans.fit(reduced_data)

print("Variance explained by first two principal components: ")
print(pcaDecomp.explained_variance_ratio_)

# Step size of the mesh. Decrease to increase the quality of the VQ.
h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use PCA model.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])


Z = Z.reshape(xx.shape)
plt.figure()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')

plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
# Plot the centroids as a white X
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
plt.title('K-means clustering of stations (PCA-reduced data)')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.savefig("clusterStations.png")