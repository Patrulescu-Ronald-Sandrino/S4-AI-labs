import csv
import random
from typing import List, Dict, Any

import numpy as np
import texttable
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
            temp_cent = -1  # TODO: replace -1
            centroids.append(temp_cent)

        # updated centroids

        points = np.array([np.argmin(distance) for distance in distances])

    return points


def create_results_table() -> str:
    table: texttable.Texttable = texttable.Texttable()
    averages = {'accuracy': 0.0, 'precision': 0.0, 'rappel': 0.0, 'score': 0.0}
    labels = ['A', 'B', 'C', 'D']  # TODO:

    table.add_row([" "] + list(averages.keys()))
    for label in labels:  # Cursul 9 slide-ul 24
        true_positive, true_negative, false_positive, false_negative = random.randint(2, 10), 1, 2, 3  # TODO replace 0, 1, 2, 3
        accuracy: float = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
        precision: float = true_positive / (true_positive + false_positive)
        rappel: float = true_positive / (true_positive + false_negative)
        score: float = 2 * precision * rappel / (precision + rappel)

        averages['accuracy'] += accuracy
        averages['precision'] += precision
        averages['rappel'] += rappel
        averages['score'] += score

        table.add_row([label, accuracy, precision, rappel, score])

    for key, value in averages.items():
        averages[key] = value / len(labels)

    table.add_row(['AVERAGE', averages['accuracy'], averages['precision'], averages['rappel'], averages['score']])

    return table.draw()
    # header row: accuracy, precision, rappel, score,
    # header col: A, B, C, D, Average



def main():
    # load data
    # data = readPoints()
    data = []
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


if __name__ == "__main__":
    print(create_results_table())
    # main()
