import csv

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
from tqdm import trange
import matplotlib.pyplot as plt


def KMeans(x, k, no_of_iterations):
    cid = np.random.choice(len(x), k, replace=False)
    # choose random centroids
    centroids = x[cid, :]

    # distance between centroids and all the data points
    distances = cdist(x, centroids, 'euclidean')

    # Centroid with the minimum distance
    points = np.array()

    for times in trange(no_of_iterations):
        centroids = []
        for cid in range(k):
            # updating centroids by taking mean of cluster it belongs to
            temp_cent =
            centroids.append(temp_cent)

        # updated centroids

        points = np.array([np.argmin(distance) for distance in distances])

    return points


def readPoints():
    points = []
    with open('dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # Complete appending point (row1, row2) to points list
    return points


if __name__ == "__main__":
    # load data
    data = readPoints()
    # Use skikit learns PCA s
    pca = PCA(2)

    # transform the data aka fit the model with X and apply the dimensionality reduction on X
    df = pca.fit_transform(data)

    label = KMeans(df, 4, 1000)

    u_labels = np.unique(label)
    for i in u_labels:
        # Complete the scatter plot
        plt.scatter()
    plt.legend()
    plt.show()
