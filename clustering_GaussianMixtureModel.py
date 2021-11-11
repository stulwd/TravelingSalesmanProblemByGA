import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import numpy as np


def label(cityData):
    X = np.array(cityData)
    gmm = GaussianMixture(n_components=3, covariance_type='full').fit(X)
    y_pred = gmm.predict(X)
    return y_pred
